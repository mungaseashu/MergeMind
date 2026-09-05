from app.graph.neo4j_client import neo4j_client

class RelationshipBuilder:
    def __init__(self):
        pass

    def link_repository_to_directory(self, repo_id: str, dir_id: str):
        query = """
        MATCH (r:Repository {id: $repo_id}), (d:Directory {id: $dir_id})
        MERGE (r)-[:CONTAINS]->(d)
        """
        with neo4j_client.get_session() as session:
            session.run(query, repo_id=repo_id, dir_id=dir_id)

    def link_repository_to_file(self, repo_id: str, file_id: str):
        query = """
        MATCH (r:Repository {id: $repo_id}), (f:File {id: $file_id})
        MERGE (r)-[:CONTAINS]->(f)
        """
        with neo4j_client.get_session() as session:
            session.run(query, repo_id=repo_id, file_id=file_id)

    def link_directory_to_directory(self, parent_id: str, child_id: str):
        query = """
        MATCH (p:Directory {id: $parent_id}), (c:Directory {id: $child_id})
        MERGE (p)-[:CONTAINS]->(c)
        """
        with neo4j_client.get_session() as session:
            session.run(query, parent_id=parent_id, child_id=child_id)

    def link_directory_to_file(self, dir_id: str, file_id: str):
        query = """
        MATCH (d:Directory {id: $dir_id}), (f:File {id: $file_id})
        MERGE (d)-[:CONTAINS]->(f)
        """
        with neo4j_client.get_session() as session:
            session.run(query, dir_id=dir_id, file_id=file_id)

    def link_file_to_class(self, file_id: str, class_id: str):
        query = """
        MATCH (f:File {id: $file_id}), (c:Class {id: $class_id})
        MERGE (f)-[:DEFINES]->(c)
        """
        with neo4j_client.get_session() as session:
            session.run(query, file_id=file_id, class_id=class_id)

    def link_file_to_function(self, file_id: str, func_id: str):
        query = """
        MATCH (f:File {id: $file_id}), (fn:Function {id: $func_id})
        MERGE (f)-[:DEFINES]->(fn)
        """
        with neo4j_client.get_session() as session:
            session.run(query, file_id=file_id, func_id=func_id)

    def link_class_to_method(self, class_id: str, func_id: str):
        query = """
        MATCH (c:Class {id: $class_id}), (fn:Function {id: $func_id})
        MERGE (c)-[:HAS_METHOD]->(fn)
        """
        with neo4j_client.get_session() as session:
            session.run(query, class_id=class_id, func_id=func_id)

    def link_class_inherits(self, child_class_id: str, parent_class_name: str):
        # We might only know the parent class by name initially. 
        # A more advanced pass would resolve the name to a specific class ID.
        # For now, we create a pseudo-node or resolve if possible.
        query = """
        MATCH (child:Class {id: $child_id})
        MERGE (parent:Class {name: $parent_name}) // simplified resolution
        MERGE (child)-[:INHERITS]->(parent)
        """
        with neo4j_client.get_session() as session:
            session.run(query, child_id=child_class_id, parent_name=parent_class_name)

    def link_file_imports_module(self, file_id: str, module_name: str):
        # Could be an external package or a local module.
        query = """
        MATCH (f:File {id: $file_id})
        MERGE (m:Module {id: $module_name, name: $module_name})
        MERGE (f)-[:IMPORTS]->(m)
        """
        with neo4j_client.get_session() as session:
            session.run(query, file_id=file_id, module_name=module_name)

    def link_function_calls(self, caller_id: str, called_name: str):
        query = """
        MATCH (caller:Function {id: $caller_id})
        MERGE (called:Function {name: $called_name}) // simplified resolution
        MERGE (caller)-[:CALLS]->(called)
        """
        with neo4j_client.get_session() as session:
            session.run(query, caller_id=caller_id, called_name=called_name)

    def link_endpoint_to_function(self, endpoint_id: str, func_id: str):
        query = """
        MATCH (e:Endpoint {id: $endpoint_id}), (f:Function {id: $func_id})
        MERGE (e)-[:IMPLEMENTED_BY]->(f)
        """
        with neo4j_client.get_session() as session:
            session.run(query, endpoint_id=endpoint_id, func_id=func_id)

    def link_pr_to_repository(self, pr_id: str, repo_id: str):
        """Links a PullRequest to its target Repository."""
        query = """
        MATCH (pr:PullRequest {id: $pr_id}), (r:Repository {id: $repo_id})
        MERGE (pr)-[:TARGETS]->(r)
        """
        with neo4j_client.get_session() as session:
            session.run(query, pr_id=pr_id, repo_id=repo_id)

    def link_pr_to_file(self, pr_id: str, file_id: str):
        """Links a PullRequest to a File that it modifies."""
        query = """
        MATCH (pr:PullRequest {id: $pr_id}), (f:File {id: $file_id})
        MERGE (pr)-[:MODIFIES]->(f)
        """
        with neo4j_client.get_session() as session:
            session.run(query, pr_id=pr_id, file_id=file_id)

