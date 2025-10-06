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

Respond with ONLY the intent word: explain, debug, or suggest"""),
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
        
        if intent not in ["explain", "debug", "suggest"]:
            if has_code:
                return "debug"
            return "explain"
        
        return intent
