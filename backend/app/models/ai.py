from pydantic import BaseModel

class AIRequest(BaseModel):
    query: str

class AIResponse(BaseModel):
    response: str
