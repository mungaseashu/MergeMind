"""
Incremental Updater — processes only the files changed in a PR.

Instead of re-scanning the whole repository, this module:
1. Fetches the list of changed files from GitHub for a given PR number.
2. Downloads the raw content of each modified/added file.
3. Runs it through our AST parser.
4. Upserts (MERGE) the updated nodes into Neo4j.
5. DETACH DELETEs nodes for removed files.
"""

import os
from typing import List, Dict
from github import Github, Auth
from app.core.config import settings
from app.parsers.python_parser import PythonASTParser
from app.graph.neo4j_client import neo4j_client
from app.graph.node_builder import NodeBuilder
from app.graph.relationship_builder import RelationshipBuilder
from app.models.code_entities import FileModel, ClassModel, FunctionModel, EndpointModel


def _get_github_client() -> Github:
    if settings.GITHUB_TOKEN:
        return Github(auth=Auth.Token(settings.GITHUB_TOKEN))
    return Github()


def get_changed_files(repo_full_name: str, pr_number: int) -> List[Dict]:
    """
    Queries the GitHub API to get the list of files changed in a specific PR.

    Returns a list of dicts with keys:
        - filename (str): path relative to repo root, e.g. 'app/api/brain.py'
        - status (str): 'added' | 'modified' | 'removed' | 'renamed'
        - raw_url (str): Direct URL to download the file's content at the PR's head commit
    """
    g = _get_github_client()
    repo = g.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    changed = []
    for f in pr.get_files():
        changed.append({
            "filename": f.filename,
            "status": f.status,
            "raw_url": f.raw_url,
            "patch": f.patch  # The unified diff (useful for future risk scoring)
        })
    return changed


def process_changed_files(repo_id: str, changed_files: List[Dict]):
    """
    Processes the changed file list and updates the Neo4j graph accordingly.

    - For 'added' or 'modified' Python files: re-parses and upserts nodes.
    - For 'removed' files: DETACH DELETEs the File node and its entities.
    - Non-Python files still get their File node created/updated, just no AST parsing.
    """
    nb = NodeBuilder()
    rb = RelationshipBuilder()
    neo4j_client.connect()

    g = _get_github_client()

    stats = {"upserted": 0, "deleted": 0, "skipped": 0, "errors": []}

    for f in changed_files:
        filename = f["filename"]
        status = f["status"]
        file_id = f"file:{repo_id}:{filename}"
        extension = os.path.splitext(filename)[1].lower()
        language = "python" if extension == ".py" else "unknown"

        if status == "removed":
            nb.delete_file_entities(file_id)
            stats["deleted"] += 1
            continue

        # For added / modified / renamed: download and process the file
        try:
            import requests
            response = requests.get(f["raw_url"], timeout=15)
            response.raise_for_status()
            source_code = response.text
        except Exception as e:
            stats["errors"].append({"file": filename, "error": f"Download failed: {e}"})
            stats["skipped"] += 1
            continue

        # Upsert the File node
        file_model = FileModel(
            id=file_id,
            repository_id=repo_id,
            path=filename,
            name=os.path.basename(filename),
            extension=extension,
            language=language,
            size_bytes=len(source_code.encode("utf-8")),
            line_count=len(source_code.splitlines()),
            hash="",
            last_modified=0.0
        )
        nb.create_file(file_model)

        # Parse Python files
        if language == "python":
            try:
                parser = PythonASTParser(source_code, filename)
                parse_result = parser.parse()

                if "error" in parse_result:
                    stats["errors"].append({"file": filename, "error": parse_result["error"]})
                    stats["skipped"] += 1
                    continue

                for cls in parse_result.get("classes", []):
                    class_id = f"class:{repo_id}:{filename}:{cls['name']}"
                    nb.create_class(ClassModel(
                        id=class_id, name=cls["name"], file_id=file_id,
                        start_line=cls["start_line"], end_line=cls["end_line"],
                        docstring=cls["docstring"]
                    ))
                    rb.link_file_to_class(file_id, class_id)
                    for parent in cls.get("inherits", []):
                        rb.link_class_inherits(class_id, parent)

                for func in parse_result.get("functions", []):
                    class_name = func.get("class_name")
                    func_id = f"function:{repo_id}:{filename}:{func['name']}"
                    class_id = f"class:{repo_id}:{filename}:{class_name}" if class_name else None

                    nb.create_function(FunctionModel(
                        id=func_id, name=func["name"], file_id=file_id, class_id=class_id,
                        start_line=func["start_line"], end_line=func["end_line"],
                        docstring=func["docstring"], is_async=func.get("is_async", False)
                    ))
                    if class_id:
                        rb.link_class_to_method(class_id, func_id)
                    else:
                        rb.link_file_to_function(file_id, func_id)

                    if func.get("is_endpoint"):
                        endpoint_id = f"endpoint:{repo_id}:{func['endpoint_method']}:{func['endpoint_path']}"
                        nb.create_endpoint(EndpointModel(
                            id=endpoint_id, method=func["endpoint_method"],
                            path=func["endpoint_path"], file_id=file_id, function_id=func_id
                        ))
                        rb.link_endpoint_to_function(endpoint_id, func_id)

                for imp in parse_result.get("imports", []):
                    rb.link_file_imports_module(file_id, imp["module"])

            except Exception as e:
                stats["errors"].append({"file": filename, "error": str(e)})
                stats["skipped"] += 1
                continue

        stats["upserted"] += 1

    return stats
