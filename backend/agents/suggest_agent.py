from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class SuggestAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.6)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming mentor. Your job is to suggest related problems and practice recommendations.

Provide:
1. Similar problems by topic/algorithm
2. Problems that build on the same concepts
3. Difficulty progression suggestions
4. Specific problem names from popular platforms (LeetCode, Codeforces, CodeChef, AtCoder)
5. Topics to study to solve similar problems

Be specific and actionable."""),
            ("user", """Platform: {site}
Current Problem: {title}
Problem Statement:
{problem}

User's Question: {question}

Please suggest similar problems or next steps for practice.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, title: str, problem: str, question: str) -> str:
        return self.chain.invoke({
            "site": site,
            "title": title,
            "problem": problem,
            "question": question
        })
