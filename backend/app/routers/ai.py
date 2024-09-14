from fastapi import APIRouter
from app.models import ai as ai_model

router = APIRouter()

@router.post("/ai", response_model=ai_model.AIResponse)
def handle_ai_query(request: ai_model.AIRequest):
    # Simple AI response logic
    response_text = f"AI received your query: {request.query}"
    return ai_model.AIResponse(response=response_text)
