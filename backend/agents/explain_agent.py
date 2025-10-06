from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class ExplainAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.5)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming tutor. Your job is to explain coding problems in simple, clear terms.
            
Break down the problem into:
1. What the problem is asking
2. Key constraints and edge cases
3. A high-level approach (without giving away the full solution)
4. Time and space complexity considerations

Be encouraging and educational."""),
            ("user", """Platform: {site}
Problem Title: {title}
Problem Statement:
{problem}

User's Question: {question}

Please explain this problem clearly.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, title: str, problem: str, question: str) -> str:
        return self.chain.invoke({
            "site": site,
            "title": title,
            "problem": problem,
            "question": question
        })
