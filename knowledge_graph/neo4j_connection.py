import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")


class Neo4jConnection:

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

    def verify_connection(self):
        try:
            self.driver.verify_connectivity()
            return {
                "status": "connected",
                "message": "Neo4j connection successful",
                "database": NEO4J_DATABASE,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

    def close(self):
        self.driver.close()


neo4j_connection = Neo4jConnection()