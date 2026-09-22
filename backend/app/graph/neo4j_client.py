from neo4j import GraphDatabase, Driver
from app.core.config import settings

class Neo4jClient:
    def __init__(self):
        self.driver: Driver | None = None

    def connect(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            # Warm up schema to prevent UNRECOGNIZED warnings for PullRequest properties
            try:
                with self.driver.session() as session:
                    session.run("MERGE (pr:PullRequest {id: 'dummy'}) SET pr.title='', pr.author='', pr.status='', pr.created_at=0, pr.pr_number=0 WITH pr MERGE (r:Repository {id:'dummy'}) MERGE (pr)-[:TARGETS]->(r) DETACH DELETE pr")
            except Exception:
                pass

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def get_session(self):
        if not self.driver:
            self.connect()
        return self.driver.session()

neo4j_client = Neo4jClient()
