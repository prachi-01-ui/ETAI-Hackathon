from fastapi import APIRouter, HTTPException

from rag.rag_service import rag_service


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.get("/status")
def get_rag_status():
    return {
        "status": "operational",
        "documents_loaded": len(rag_service.documents),
        "sources": [
            document["source"]
            for document in rag_service.documents
        ],
    }


@router.get("/search")
def search_knowledge(query: str):
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty",
        )

    results = rag_service.retrieve(query)

    return {
        "query": query,
        "results_found": len(results),
        "results": results,
    }