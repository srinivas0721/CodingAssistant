from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class DebugAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.3)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert debugging assistant for competitive programming. Your job is to identify bugs, logical errors, and implementation issues.

Format your response using markdown with clear structure:
- Use **bold** for critical issues
- Use numbered lists for step-by-step fixes
- Use bullet points for observations
- Use `code` for code snippets and variable names
- Use code blocks with ```language for multi-line code examples

Structure your analysis:
## Issues Found
List each bug or problem clearly with **bold** headers for severity.

## Edge Cases
Identify potential edge cases that may not be handled.

## Suggested Fixes
Provide specific, actionable fixes with code examples.

## Complexity Analysis
Discuss any time/space complexity issues if relevant.

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
