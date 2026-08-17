from app.graph.neo4j_client import neo4j_client

def setup_constraints():
    constraints = [
        "CREATE CONSTRAINT repository_id_unique IF NOT EXISTS FOR (n:Repository) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT directory_id_unique IF NOT EXISTS FOR (n:Directory) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT file_id_unique IF NOT EXISTS FOR (n:File) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT class_id_unique IF NOT EXISTS FOR (n:Class) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT function_id_unique IF NOT EXISTS FOR (n:Function) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT module_id_unique IF NOT EXISTS FOR (n:Module) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT package_name_unique IF NOT EXISTS FOR (n:Package) REQUIRE n.name IS UNIQUE",
        "CREATE CONSTRAINT endpoint_id_unique IF NOT EXISTS FOR (n:Endpoint) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT database_id_unique IF NOT EXISTS FOR (n:Database) REQUIRE n.id IS UNIQUE",
        "CREATE CONSTRAINT table_id_unique IF NOT EXISTS FOR (n:Table) REQUIRE n.id IS UNIQUE",
    ]

    with neo4j_client.get_session() as session:
        for query in constraints:
            try:
                session.run(query)
                print(f"Executed constraint: {query}")
            except Exception as e:
                print(f"Error executing constraint: {e}")

if __name__ == "__main__":
    neo4j_client.connect()
    setup_constraints()
    neo4j_client.close()
