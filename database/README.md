# Database Layer

The Energy Supply Chain Resilience Platform uses a hybrid data architecture.

## Relational Database

SQLAlchemy is used by the FastAPI backend for transactional and operational data including:

- Risk Events
- Simulation Runs
- Recommendations
- Decision Actions
- Action Outcomes
- Suppliers
- Procurement
- Inventory
- Strategic Reserves

The database connection and SQLAlchemy session management are implemented in:

`backend/database.py`

## Graph Database

Neo4j Aura is used for the Energy Supply Chain Knowledge Graph.

It represents relationships between:

Supplier → Port → Shipping Route → Destination Port → Refinery

Risk events are connected to affected supply-chain assets through graph relationships.

Neo4j integration is implemented in:

`knowledge_graph/neo4j_connection.py`

`knowledge_graph/neo4j_service.py`

## Architecture

Relational Database
→ Operational and transactional records

Neo4j Knowledge Graph
→ Supply-chain dependencies and risk relationships