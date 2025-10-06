from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class SolverAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.3)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming solver. Your job is to provide complete, working code solutions.

Format your response using markdown with clear structure:
- Use **bold** for important concepts
- Use `code` for algorithm names and complexity
- Use code blocks with ```language for the solution code
- Provide clear explanations

Structure your solution:
## Approach
Explain the algorithm and strategy in 2-3 sentences.

## Complexity Analysis
- **Time Complexity**: O(?)
- **Space Complexity**: O(?)

## Solution Code
```{language}
[Complete working code here]
```

## Explanation
Walk through the key parts of the code and why they work.

Be clear, concise, and ensure the code is correct and efficient."""),
            ("user", """Platform: {site}
Problem Title: {title}
Problem Statement:
{problem}

Programming Language: {language}
User's Question: {question}

Please provide a complete working solution in {language}.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, title: str, problem: str, language: str, question: str) -> str:
        return self.chain.invoke({
            "site": site,
            "title": title,
            "problem": problem,
            "language": language,
            "question": question
        })
