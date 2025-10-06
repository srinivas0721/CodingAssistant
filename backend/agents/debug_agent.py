from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class DebugAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.3)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert debugging assistant for competitive programming. Your job is to identify bugs, logical errors, and implementation issues.

Analyze the code and:
1. Identify potential bugs or logical errors
2. Check for edge cases that might not be handled
3. Look for time/space complexity issues
4. Suggest specific fixes or improvements
5. Provide hints rather than complete solutions when appropriate

Be precise and actionable."""),
            ("user", """Platform: {site}
Problem: {problem}
Language: {language}

User's Code:
```{language}
{code}
```

User's Question: {question}

Please help debug this code.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, problem: str, code: str, language: str, question: str) -> str:
        return self.chain.invoke({
            "site": site,
            "problem": problem,
            "code": code,
            "language": language,
            "question": question
        })
