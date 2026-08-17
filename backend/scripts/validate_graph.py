import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from app.graph.neo4j_client import neo4j_client

def validate_graph():
    neo4j_client.connect()
    
    queries = {
        "Repositories": "MATCH (n:Repository) RETURN count(n) as count",
        "Directories": "MATCH (n:Directory) RETURN count(n) as count",
        "Files": "MATCH (n:File) RETURN count(n) as count",
        "Classes": "MATCH (n:Class) RETURN count(n) as count",
        "Functions": "MATCH (n:Function) RETURN count(n) as count",
        "Endpoints": "MATCH (n:Endpoint) RETURN count(n) as count",
        "Modules": "MATCH (n:Module) RETURN count(n) as count",
        "Relationships": "MATCH ()-[r]->() RETURN count(r) as count"
    }

    print("--- GRAPH STATISTICS ---")
    with neo4j_client.get_session() as session:
        for label, query in queries.items():
            result = session.run(query)
            record = result.single()
            print(f"{label}: {record['count']}")

    print("\n--- SAMPLE IMPORTS ---")
    import_query = "MATCH (a:File)-[:IMPORTS]->(b:Module) RETURN a.name, b.name LIMIT 5"
    with neo4j_client.get_session() as session:
        result = session.run(import_query)
        for record in result:
            print(f"{record['a.name']} -> {record['b.name']}")

    neo4j_client.close()

if __name__ == "__main__":
    validate_graph()
