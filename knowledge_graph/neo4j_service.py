import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class Neo4jService:

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE")

        self.driver = None

        if self.uri and self.username and self.password:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )

    def verify_connection(self):
        if not self.driver:
            return False

        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            print("Neo4j connection error:", e)
            return False

    def close(self):
        if self.driver:
            self.driver.close()
            
    def create_supply_chain_graph(self):
        if not self.driver:
            return {
                "status": "error",
                "message": "Neo4j driver is not connected"
            }

        query = """
        MERGE (supplier:Supplier {name: 'Middle East Crude Supplier'})
        SET supplier.region = 'Middle East',
            supplier.commodity = 'Crude Oil'

        MERGE (origin:Port {name: 'Ras Tanura Port'})
        SET origin.country = 'Saudi Arabia'

        MERGE (route:ShippingRoute {name: 'Strait of Hormuz Route'})
        SET route.risk_level = 'Critical',
            route.risk_score = 87

        MERGE (destination:Port {name: 'Mundra Port'})
        SET destination.country = 'India'

        MERGE (refinery:Refinery {name: 'Indian Energy Refinery'})
        SET refinery.country = 'India'

        MERGE (risk:RiskEvent {name: 'Strait of Hormuz Disruption'})
        SET risk.severity = 'Critical',
            risk.risk_score = 87,
            risk.type = 'Geopolitical'

        MERGE (supplier)-[:SUPPLIES_TO]->(origin)
        MERGE (origin)-[:CONNECTS_TO]->(route)
        MERGE (route)-[:ARRIVES_AT]->(destination)
        MERGE (destination)-[:SUPPLIES_TO]->(refinery)
        MERGE (risk)-[:THREATENS]->(route)

        RETURN supplier, origin, route, destination, refinery, risk
        """

        try:
            with self.driver.session(database=self.database) as session:
                session.run(query).consume()

            return {
                "status": "success",
                "message": "Supply chain knowledge graph created"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }   

    def get_supply_chain_graph(self):
        """
        Read supply-chain nodes and relationships directly
        from Neo4j for frontend D3 visualization.
        """

        if not self.driver:
            return {
                "status": "error",
                "message": "Neo4j driver is not connected"
            }

        query = """
        MATCH (source)-[relationship]->(target)
        RETURN
            elementId(source) AS source_id,
            labels(source) AS source_labels,
            properties(source) AS source_properties,

            type(relationship) AS relationship_type,

            elementId(target) AS target_id,
            labels(target) AS target_labels,
            properties(target) AS target_properties
        """

        try:
            nodes = {}
            links = []

            with self.driver.session(
                database=self.database
            ) as session:

                result = session.run(query)

                for record in result:

                    source_id = record["source_id"]
                    target_id = record["target_id"]

                    source_labels = record["source_labels"]
                    target_labels = record["target_labels"]

                    source_properties = dict(
                        record["source_properties"]
                    )

                    target_properties = dict(
                        record["target_properties"]
                    )

                    # Add source node only once
                    if source_id not in nodes:
                        nodes[source_id] = {
                            "id": source_id,
                            "label": source_properties.get(
                                "name",
                                source_id
                            ),
                            "type": (
                                source_labels[0]
                                if source_labels
                                else "Unknown"
                            ),
                            "properties": source_properties,
                        }

                    # Add target node only once
                    if target_id not in nodes:
                        nodes[target_id] = {
                            "id": target_id,
                            "label": target_properties.get(
                                "name",
                                target_id
                            ),
                            "type": (
                                target_labels[0]
                                if target_labels
                                else "Unknown"
                            ),
                            "properties": target_properties,
                        }

                    # Add relationship
                    links.append({
                        "source": source_id,
                        "target": target_id,
                        "type": record[
                            "relationship_type"
                        ],
                    })

            return {
                "status": "success",
                "nodes": list(nodes.values()),
                "links": links,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
            }

neo4j_service = Neo4jService()