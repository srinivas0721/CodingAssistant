from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class ExplainAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.5)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming tutor. Your job is to explain coding problems in simple, clear terms.

Format your response using markdown with clear structure:
- Use **bold** for important concepts
- Use numbered lists for sequential steps
- Use bullet points for key points
- Use `code` formatting for technical terms

Break down the problem into clear sections:
## 1. What the Problem is Asking
Explain the core problem in simple terms.

## 2. Key Constraints and Edge Cases
List important constraints and potential edge cases.

## 3. High-Level Approach
Provide a conceptual approach without giving away the full solution.

## 4. Time and Space Complexity
Discuss complexity considerations.

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
