import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.ingestion.scanner import RepositoryScanner
from app.parsers.python_parser import PythonASTParser
from app.graph.neo4j_client import neo4j_client
from app.graph.constraints import setup_constraints
from app.graph.node_builder import NodeBuilder
from app.graph.relationship_builder import RelationshipBuilder
from app.models.code_entities import (
    DirectoryModel, FileModel, ClassModel, FunctionModel, EndpointModel
)

def run_seed(repo_path: str, repo_name: str):
    print(f"Connecting to Neo4j...")
    neo4j_client.connect()
    
    print("Setting up constraints...")
    setup_constraints()

    nb = NodeBuilder()
    rb = RelationshipBuilder()

    repo_id = f"repo:local:{repo_name}"
    nb.create_repository(repo_id=repo_id, name=repo_name)

    print(f"Scanning repository at {repo_path}...")
    scanner = RepositoryScanner(repo_path)
    scan_result = scanner.scan()

    dirs = scan_result["directories"]
    files = scan_result["files"]

    print(f"Found {len(dirs)} directories and {len(files)} files.")

    # Build Directories
    for d in dirs:
        dir_id = f"dir:{repo_id}:{d['path']}"
        dir_model = DirectoryModel(id=dir_id, repository_id=repo_id, path=d['path'], name=d['name'])
        nb.create_directory(dir_model)
        
        # simplified parent linking
        parent_path = str(Path(d['path']).parent).replace("\\", "/")
        if parent_path == ".":
            rb.link_repository_to_directory(repo_id, dir_id)
        else:
            parent_id = f"dir:{repo_id}:{parent_path}"
            rb.link_directory_to_directory(parent_id, dir_id)

    # Build Files and Parse Python
    for f in files:
        file_id = f"file:{repo_id}:{f['path']}"
        file_model = FileModel(
            id=file_id, repository_id=repo_id, path=f['path'], name=f['name'],
            extension=f['extension'], language=f['language'], size_bytes=f['size_bytes'],
            line_count=0, hash="", last_modified=f['last_modified']
        )
        nb.create_file(file_model)

        parent_path = str(Path(f['path']).parent).replace("\\", "/")
        if parent_path == ".":
            rb.link_repository_to_file(repo_id, file_id)
        else:
            parent_id = f"dir:{repo_id}:{parent_path}"
            rb.link_directory_to_file(parent_id, file_id)

        # Parse Python files
        if f['language'] == 'python':
            with open(f['absolute_path'], 'r', encoding='utf-8') as source_file:
                source_code = source_file.read()
            
            parser = PythonASTParser(source_code, f['path'])
            parse_result = parser.parse()
            
            # Update file line count
            file_model.line_count = parse_result.get('line_count', 0)
            nb.create_file(file_model) # Update
            
            # Classes
            for cls in parse_result.get("classes", []):
                class_id = f"class:{repo_id}:{f['path']}:{cls['name']}:{cls['start_line']}"
                class_model = ClassModel(
                    id=class_id, name=cls['name'], file_id=file_id,
                    start_line=cls['start_line'], end_line=cls['end_line'], docstring=cls['docstring']
                )
                nb.create_class(class_model)
                rb.link_file_to_class(file_id, class_id)

                for parent in cls.get("inherits", []):
                    rb.link_class_inherits(class_id, parent)

            # Functions / Methods
            for func in parse_result.get("functions", []):
                class_name = func.get("class_name")
                # This simplistic ID generation might need class context
                func_qual_name = f"{class_name}.{func['name']}" if class_name else func['name']
                func_id = f"function:{repo_id}:{f['path']}:{func_qual_name}:{func['start_line']}"
                
                class_id = None
                if class_name:
                    # In a real implementation we would resolve the exact class ID
                    class_id = f"class:{repo_id}:{f['path']}:{class_name}:unknown"

                func_model = FunctionModel(
                    id=func_id, name=func['name'], file_id=file_id, class_id=class_id,
                    start_line=func['start_line'], end_line=func['end_line'], 
                    docstring=func['docstring'], is_async=func.get('is_async', False)
                )
                nb.create_function(func_model)
                
                if class_name:
                    # simplistic link, would need real class_id
                    rb.link_class_to_method(class_id, func_id)
                else:
                    rb.link_file_to_function(file_id, func_id)

                # Endpoints
                if func.get("is_endpoint"):
                    endpoint_id = f"endpoint:{repo_id}:{func['endpoint_method']}:{func['endpoint_path']}"
                    endpoint_model = EndpointModel(
                        id=endpoint_id, method=func['endpoint_method'], path=func['endpoint_path'],
                        file_id=file_id, function_id=func_id
                    )
                    nb.create_endpoint(endpoint_model)
                    rb.link_endpoint_to_function(endpoint_id, func_id)

            # Imports
            for imp in parse_result.get("imports", []):
                rb.link_file_imports_module(file_id, imp['module'])

            # Calls
            for call in parse_result.get("calls", []):
                # We don't have the caller context natively mapped in this simple script easily
                pass 

    print("Indexing complete.")
    neo4j_client.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python seed_test_repository.py <repo_path> <repo_name>")
        sys.exit(1)
    run_seed(sys.argv[1], sys.argv[2])
