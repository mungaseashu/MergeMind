from app.graph.neo4j_client import neo4j_client
from app.models.code_entities import (
    DirectoryModel, FileModel, ClassModel, FunctionModel, EndpointModel
)

class NodeBuilder:
    def __init__(self):
        pass

    def create_repository(self, repo_id: str, name: str, url: str = ""):
        query = """
        MERGE (r:Repository {id: $repo_id})
        SET r.name = $name,
            r.github_url = $url,
            r.indexed_at = timestamp(),
            r.status = 'COMPLETED'
        """
        with neo4j_client.get_session() as session:
            session.run(query, repo_id=repo_id, name=name, url=url)

    def create_directory(self, d: DirectoryModel):
        query = """
        MERGE (dir:Directory {id: $id})
        SET dir.path = $path,
            dir.name = $name,
            dir.repository_id = $repo_id
        """
        with neo4j_client.get_session() as session:
            session.run(query, id=d.id, path=d.path, name=d.name, repo_id=d.repository_id)

    def create_file(self, f: FileModel):
        query = """
        MERGE (file:File {id: $id})
        SET file.path = $path,
            file.name = $name,
            file.extension = $extension,
            file.language = $language,
            file.size_bytes = $size_bytes,
            file.line_count = $line_count,
            file.hash = $hash,
            file.repository_id = $repo_id,
            file.last_modified = $last_modified
        """
        with neo4j_client.get_session() as session:
            session.run(
                query, id=f.id, path=f.path, name=f.name, extension=f.extension,
                language=f.language, size_bytes=f.size_bytes, line_count=f.line_count,
                hash=f.hash, repo_id=f.repository_id, last_modified=f.last_modified
            )

    def create_class(self, c: ClassModel):
        query = """
        MERGE (cls:Class {id: $id})
        SET cls.name = $name,
            cls.file_id = $file_id,
            cls.start_line = $start_line,
            cls.end_line = $end_line,
            cls.docstring = $docstring
        """
        with neo4j_client.get_session() as session:
            session.run(
                query, id=c.id, name=c.name, file_id=c.file_id,
                start_line=c.start_line, end_line=c.end_line, docstring=c.docstring
            )

    def create_function(self, f: FunctionModel):
        query = """
        MERGE (func:Function {id: $id})
        SET func.name = $name,
            func.file_id = $file_id,
            func.class_id = $class_id,
            func.start_line = $start_line,
            func.end_line = $end_line,
            func.docstring = $docstring,
            func.is_async = $is_async
        """
        with neo4j_client.get_session() as session:
            session.run(
                query, id=f.id, name=f.name, file_id=f.file_id, class_id=f.class_id,
                start_line=f.start_line, end_line=f.end_line, docstring=f.docstring,
                is_async=f.is_async
            )

    def create_endpoint(self, e: EndpointModel):
        query = """
        MERGE (endp:Endpoint {id: $id})
        SET endp.method = $method,
            endp.path = $path,
            endp.file_id = $file_id,
            endp.function_id = $function_id,
            endp.framework = $framework
        """
        with neo4j_client.get_session() as session:
            session.run(
                query, id=e.id, method=e.method, path=e.path,
                file_id=e.file_id, function_id=e.function_id, framework=e.framework
            )
