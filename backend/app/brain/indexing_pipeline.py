import uuid
import threading
from app.ingestion.repository_manager import repository_manager
from app.ingestion.scanner import RepositoryScanner
from app.parsers.python_parser import PythonASTParser
from app.graph.neo4j_client import neo4j_client
from app.graph.node_builder import NodeBuilder
from app.graph.relationship_builder import RelationshipBuilder
from app.models.code_entities import (
    DirectoryModel, FileModel, ClassModel, FunctionModel, EndpointModel
)
from pathlib import Path

# In-memory dictionary to track job statuses (In production, use Redis or DB)
indexing_jobs = {}

class IndexingPipeline:
    def __init__(self):
        self.nb = NodeBuilder()
        self.rb = RelationshipBuilder()

    def start_job(self, repo_url: str) -> str:
        job_id = str(uuid.uuid4())
        indexing_jobs[job_id] = {
            "status": "QUEUED",
            "repository_url": repo_url,
            "progress": 0,
            "files_discovered": 0,
            "files_processed": 0,
            "nodes_created": 0,
            "relationships_created": 0,
            "errors": []
        }
        
        # Start async thread
        thread = threading.Thread(target=self._run_pipeline, args=(job_id, repo_url))
        thread.start()
        
        return job_id

    def get_job_status(self, job_id: str):
        return indexing_jobs.get(job_id)

    def _update_job(self, job_id: str, **kwargs):
        if job_id in indexing_jobs:
            indexing_jobs[job_id].update(kwargs)

    def _run_pipeline(self, job_id: str, repo_url: str):
        try:
            self._update_job(job_id, status="CLONING", progress=10)
            repo_data = repository_manager.process_repository(repo_url)
            local_path = repo_data["local_path"]
            repo_info = repo_data["info"]

            neo4j_client.connect()
            
            repo_id = f"repo:{repo_info['full_name']}"
            self.nb.create_repository(repo_id=repo_id, name=repo_info['name'], url=repo_url)
            self._update_job(job_id, nodes_created=1)

            self._update_job(job_id, status="SCANNING", progress=30)
            scanner = RepositoryScanner(local_path)
            scan_result = scanner.scan()
            
            dirs = scan_result["directories"]
            files = scan_result["files"]
            
            self._update_job(job_id, files_discovered=len(files), status="ANALYZING", progress=40)
            
            nodes_created = 1
            rels_created = 0

            # 1. Directories
            for d in dirs:
                dir_id = f"dir:{repo_id}:{d['path']}"
                self.nb.create_directory(DirectoryModel(id=dir_id, repository_id=repo_id, path=d['path'], name=d['name']))
                nodes_created += 1
                
                parent_path = str(Path(d['path']).parent).replace("\\", "/")
                if parent_path == ".":
                    self.rb.link_repository_to_directory(repo_id, dir_id)
                else:
                    self.rb.link_directory_to_directory(f"dir:{repo_id}:{parent_path}", dir_id)
                rels_created += 1

            # 2. Files and Parsing
            processed = 0
            for f in files:
                file_id = f"file:{repo_id}:{f['path']}"
                file_model = FileModel(
                    id=file_id, repository_id=repo_id, path=f['path'], name=f['name'],
                    extension=f['extension'], language=f['language'], size_bytes=f['size_bytes'],
                    line_count=0, hash=f.get('hash', ''), last_modified=f['last_modified']
                )
                self.nb.create_file(file_model)
                nodes_created += 1

                parent_path = str(Path(f['path']).parent).replace("\\", "/")
                if parent_path == ".":
                    self.rb.link_repository_to_file(repo_id, file_id)
                else:
                    self.rb.link_directory_to_file(f"dir:{repo_id}:{parent_path}", file_id)
                rels_created += 1

                if f['language'] == 'python':
                    try:
                        with open(f['absolute_path'], 'r', encoding='utf-8') as src:
                            source_code = src.read()
                        
                        parser = PythonASTParser(source_code, f['path'])
                        parse_result = parser.parse()
                        
                        if 'error' not in parse_result:
                            file_model.line_count = parse_result.get('line_count', 0)
                            self.nb.create_file(file_model) # update line count

                            for cls in parse_result.get('classes', []):
                                class_id = f"class:{repo_id}:{f['path']}:{cls['name']}"
                                self.nb.create_class(ClassModel(
                                    id=class_id, name=cls['name'], file_id=file_id,
                                    start_line=cls['start_line'], end_line=cls['end_line'], docstring=cls['docstring']
                                ))
                                self.rb.link_file_to_class(file_id, class_id)
                                nodes_created += 1
                                rels_created += 1
                                
                                for parent in cls.get('inherits', []):
                                    self.rb.link_class_inherits(class_id, parent)
                                    rels_created += 1

                            for func in parse_result.get('functions', []):
                                func_id = f"function:{repo_id}:{f['path']}:{func['name']}"
                                class_name = func.get("class_name")
                                class_id = f"class:{repo_id}:{f['path']}:{class_name}" if class_name else None
                                
                                self.nb.create_function(FunctionModel(
                                    id=func_id, name=func['name'], file_id=file_id, class_id=class_id,
                                    start_line=func['start_line'], end_line=func['end_line'], docstring=func['docstring']
                                ))
                                nodes_created += 1
                                
                                if class_id:
                                    self.rb.link_class_to_method(class_id, func_id)
                                else:
                                    self.rb.link_file_to_function(file_id, func_id)
                                rels_created += 1

                                if func.get('is_endpoint'):
                                    endpoint_id = f"endpoint:{repo_id}:{func['endpoint_method']}:{func['endpoint_path']}"
                                    self.nb.create_endpoint(EndpointModel(
                                        id=endpoint_id, method=func['endpoint_method'], path=func['endpoint_path'],
                                        file_id=file_id, function_id=func_id
                                    ))
                                    self.rb.link_endpoint_to_function(endpoint_id, func_id)
                                    nodes_created += 1
                                    rels_created += 1

                            for imp in parse_result.get('imports', []):
                                self.rb.link_file_imports_module(file_id, imp['module'])
                                rels_created += 1
                                
                    except Exception as e:
                        indexing_jobs[job_id]["errors"].append({"file": f['path'], "error": str(e)})
                
                processed += 1
                self._update_job(
                    job_id, files_processed=processed, 
                    nodes_created=nodes_created, relationships_created=rels_created,
                    progress=40 + int((processed / len(files)) * 50)
                )

            self._update_job(job_id, status="COMPLETED", progress=100)
        except Exception as e:
            self._update_job(job_id, status="FAILED", progress=100, errors=[str(e)])
        finally:
            # We don't close the client in a multi-threaded app immediately,
            # connection pool handles it.
            pass

pipeline = IndexingPipeline()
