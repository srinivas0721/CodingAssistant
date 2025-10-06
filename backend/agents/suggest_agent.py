from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class SuggestAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.6)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming mentor. Your job is to suggest related problems and practice recommendations.

Format your response using markdown with clear structure:
- Use **bold** for problem names and key algorithms
- Use bullet points for problem lists
- Use numbered lists for learning progression
- Use `code` for algorithm names and data structures

Structure your recommendations:
## Similar Problems
List 3-5 related problems with:
- **Problem Name** - Brief description and difficulty
- Platform (LeetCode, Codeforces, CodeChef, AtCoder)

## Key Topics to Study
List the main topics and algorithms needed.

## Learning Progression
Suggest a difficulty progression path with specific problems.

## Practice Strategy
Provide actionable advice for mastering these concepts.

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
