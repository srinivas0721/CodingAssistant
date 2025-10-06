from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import QueryRequest, QueryResponse
from graph.workflow import CPAssistantGraph
from utils.config import get_settings
import uvicorn

app = FastAPI(title="CP Assistant API")

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cp_graph = CPAssistantGraph()

@app.get("/")
async def root():
    return {"message": "CP Assistant API is running", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

def detect_preferred_language(question: str, current_language: str) -> str:
    """Detect preferred programming language from question or fallback to current/default."""
    question_lower = question.lower()
    
    language_keywords = {
        "python": ["python", "py"],
        "cpp": ["c++", "cpp", "c plus"],
        "java": ["java"],
        "javascript": ["javascript", "js", "node"],
        "go": ["go", "golang"],
        "rust": ["rust"],
        "kotlin": ["kotlin"],
        "swift": ["swift"],
        "typescript": ["typescript", "ts"]
    }
    
    for lang, keywords in language_keywords.items():
        for keyword in keywords:
            if keyword in question_lower:
                return lang
    
    if current_language and current_language != "unknown":
        return current_language
    
    return "cpp"

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        preferred_lang = detect_preferred_language(
            request.question, 
            request.language or "cpp"
        )
        
        input_state = {
            "site": request.site,
            "problem_title": request.problem_title or "",
            "problem_statement": request.problem_statement or "",
            "user_code": request.user_code or "",
            "language": request.language or "unknown",
            "question": request.question,
            "intent": "",
            "answer": "",
            "agent_used": "",
            "preferred_language": preferred_lang,
            "hint_steps": []
        }
        
        result = cp_graph.run(input_state)
        
        return QueryResponse(
            answer=result["answer"],
            agent_used=result["agent_used"],
            intent=result["intent"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)
