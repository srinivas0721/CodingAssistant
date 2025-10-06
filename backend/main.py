from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.schemas import QueryRequest, QueryResponse
from graph.workflow import CPAssistantGraph
from utils.config import get_settings
from utils.chat_storage import chat_storage
import uvicorn
import json
import asyncio

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

async def generate_streaming_response(answer_text: str, agent_used: str, intent: str):
    """Generate streaming response token by token."""
    words = answer_text.split()
    
    for i, word in enumerate(words):
        chunk = {
            "token": word + (" " if i < len(words) - 1 else ""),
            "done": False
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.03)
    
    final_chunk = {
        "token": "",
        "done": True,
        "agent_used": agent_used,
        "intent": intent
    }
    yield f"data: {json.dumps(final_chunk)}\n\n"

@app.post("/ask/stream")
async def ask_question_stream(request: QueryRequest):
    """Streaming endpoint that sends response token-by-token."""
    try:
        preferred_lang = detect_preferred_language(
            request.question, 
            request.language or "cpp"
        )
        
        site = request.site
        title = request.problem_title or ""
        
        chat_history = chat_storage.format_history_for_prompt(site, title)
        
        chat_storage.add_message(site, title, "user", request.question)
        
        input_state = {
            "site": site,
            "problem_title": title,
            "problem_statement": request.problem_statement or "",
            "user_code": request.user_code or "",
            "language": request.language or "unknown",
            "question": request.question,
            "intent": "",
            "answer": "",
            "agent_used": "",
            "preferred_language": preferred_lang,
            "hint_steps": [],
            "chat_history": chat_history
        }
        
        result = cp_graph.run(input_state)
        
        chat_storage.add_message(site, title, "assistant", result["answer"], result["agent_used"])
        
        return StreamingResponse(
            generate_streaming_response(result["answer"], result["agent_used"], result["intent"]),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Non-streaming endpoint (backwards compatible)."""
    try:
        preferred_lang = detect_preferred_language(
            request.question, 
            request.language or "cpp"
        )
        
        site = request.site
        title = request.problem_title or ""
        
        chat_history = chat_storage.format_history_for_prompt(site, title)
        
        chat_storage.add_message(site, title, "user", request.question)
        
        input_state = {
            "site": site,
            "problem_title": title,
            "problem_statement": request.problem_statement or "",
            "user_code": request.user_code or "",
            "language": request.language or "unknown",
            "question": request.question,
            "intent": "",
            "answer": "",
            "agent_used": "",
            "preferred_language": preferred_lang,
            "hint_steps": [],
            "chat_history": chat_history
        }
        
        result = cp_graph.run(input_state)
        
        chat_storage.add_message(site, title, "assistant", result["answer"], result["agent_used"])
        
        return QueryResponse(
            answer=result["answer"],
            agent_used=result["agent_used"],
            intent=result["intent"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)
