from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model
from utils.hint_storage import HintEntry
from typing import List

class HintAgent:
    def __init__(self):
        self.model = get_gemini_model(temperature=0.4)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert competitive programming tutor who provides progressive hints. Your job is to guide students step-by-step without giving away the complete solution.

Format your response using markdown with clear structure:
- Use **bold** for key concepts
- Use numbered lists for sequential steps
- Use `code` for algorithm names and patterns
- Be encouraging and supportive

IMPORTANT RULES:
1. You are providing Hint #{hint_number} out of a progressive hint sequence
2. Previous hints and their FULL CONTENT are shown below
3. Do NOT repeat information from previous hints
4. Build upon previous hints progressively - reference what was already revealed
5. Each hint should reveal ONE new insight or step
6. NEVER give the complete solution - leave room for the student to think
7. End with: "Need more help? Ask for another hint!"

Structure your hint:
## Hint #{hint_number}

[Provide ONE specific, actionable insight that builds on previous hints]

**Think about**: [A guiding question to help them apply this hint]

Need more help? Ask for another hint!

Be patient, encouraging, and pedagogical. Help them learn, don't just solve it for them."""),
            ("user", """Platform: {site}
Problem Title: {title}
Problem Statement:
{problem}

{previous_hints_content}

User's Question: {question}

Please provide Hint #{hint_number} that builds on the previous hints without repeating them.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, title: str, problem: str, hint_number: int, 
            previous_hints: List[HintEntry], question: str) -> str:
        
        if not previous_hints:
            previous_hints_content = "Hint Number: 1 (First hint)\nNo previous hints have been given yet."
        else:
            hints_text = []
            for entry in previous_hints:
                hints_text.append(f"=== Previous Hint #{entry.hint_number} ===\n{entry.hint_text}\n")
            previous_hints_content = f"Hint Number: {hint_number}\n\nPREVIOUS HINTS (DO NOT REPEAT):\n" + "\n".join(hints_text)
        
        return self.chain.invoke({
            "site": site,
            "title": title,
            "problem": problem,
            "hint_number": hint_number,
            "previous_hints_content": previous_hints_content,
            "question": question
        })
