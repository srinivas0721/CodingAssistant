from pydantic import BaseModel
from typing import Optional, Literal

class QueryRequest(BaseModel):
    site: str
    problem_title: Optional[str] = None
    problem_statement: Optional[str] = None
    user_code: Optional[str] = None
    language: Optional[str] = None
    question: str

class QueryResponse(BaseModel):
    answer: str
    agent_used: str
    intent: str
