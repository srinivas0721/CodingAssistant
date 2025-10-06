from langchain_google_genai import ChatGoogleGenerativeAI
from .config import get_settings

def get_gemini_model(temperature: float = 0.7):
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        api_key=settings.google_api_key,
        temperature=temperature,
        max_tokens=2048
    )
