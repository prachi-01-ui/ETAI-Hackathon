from fastapi import APIRouter, HTTPException

from knowledge_graph.neo4j_service import neo4j_service


router = APIRouter(
    prefix="/knowledge-graph",
    tags=["Knowledge Graph"],
)


# CHECK NEO4J CONNECTION
@router.get("/status")
def get_knowledge_graph_status():

    connected = neo4j_service.verify_connection()

    if not connected:
        raise HTTPException(
            status_code=503,
            detail="Neo4j database is not connected",
        )

    return {
        "status": "connected",
        "message": "Neo4j Knowledge Graph is operational",
    }


# CREATE / INITIALIZE SUPPLY CHAIN GRAPH
@router.post("/initialize")
def initialize_supply_chain_graph():

    result = neo4j_service.create_supply_chain_graph()

    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail=result.get("message"),
        )

    return result

# ============================================================
# GET SUPPLY CHAIN KNOWLEDGE GRAPH
# GET /knowledge-graph/graph
# ============================================================

@router.get("/graph")
def get_supply_chain_graph():

    result = neo4j_service.get_supply_chain_graph()

    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail=result.get("message"),
        )

    return result