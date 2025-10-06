from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class IntentClassifier:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.1)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an intent classifier for a competitive programming assistant.

Classify the user's question into ONE of these intents:
- "explain" - User wants the problem explained or clarified
- "debug" - User wants help finding bugs or errors in their code
- "suggest" - User wants similar problem recommendations or practice suggestions
- "solve" - User wants a complete code solution (keywords: "solve", "solution", "code for", "write code", "complete code")
- "hint" - User wants a hint or clue (keywords: "hint", "clue", "help me figure", "guide me", "push in right direction")
- "query" - User has doubts about previous conversation, asking follow-up questions, or general questions (keywords: "what did you mean", "can you clarify", "explain that again", "what was", "you said", "earlier", "previous", "before")

Respond with ONLY the intent word: explain, debug, suggest, solve, hint, or query"""),
            ("user", """User's Question: {question}
Has Code: {has_code}

Intent:""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def classify(self, question: str, has_code: bool) -> str:
        result = self.chain.invoke({
            "question": question,
            "has_code": "yes" if has_code else "no"
        })
        intent = result.strip().lower()
        
        valid_intents = ["explain", "debug", "suggest", "solve", "hint", "query"]
        if intent not in valid_intents:
            return "query"
        
        return intent
