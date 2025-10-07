from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.gemini_client import get_gemini_model

class QueryAgent:
    """Agent that answers questions about previous conversation and general doubts."""
    
    def __init__(self):
        self.model = get_gemini_model(temperature=0.5)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are QueryAgent, a helpful assistant that clarifies doubts and answers follow-up questions.

CRITICAL: You MUST format your response using proper markdown structure with clear sections and formatting:
- Use **bold** for important concepts and emphasis
- Use `code blocks` for algorithm names, code examples, and technical terms
- Use numbered lists for sequential steps or ordered information
- Use bullet points for key points and unordered lists
- Use ## headers for sections when providing detailed explanations
- ALWAYS start with a brief direct answer, then elaborate if needed

Your task is to:
1. Reference previous conversation if relevant
2. Clarify any doubts about explanations, hints, or solutions from earlier messages
3. Answer general algorithmic questions (e.g., "can I use binary search?")
4. Provide additional context or examples if needed

Structure your response clearly with proper markdown formatting. If the question is simple, give a concise answer. If it requires explanation, use sections with headers."""),
            ("user", """Platform: {site}
Problem Title: {title}
Problem Statement:
{problem}

**Previous Conversation:**
{chat_history}

**User's Question:**
{question}

Please answer the user's question based on the context and conversation history above.""")
        ])
        
        self.chain = self.prompt_template | self.model | StrOutputParser()
    
    def run(self, site: str, title: str, problem: str, question: str, chat_history: str) -> str:
        """
        Answer user's doubts based on previous conversation or general questions about the problem.
        
        Args:
            site: The coding platform (leetcode, codeforces, codechef)
            title: Problem title
            problem: Problem statement
            question: User's question
            chat_history: Formatted chat history (last 15 messages)
        
        Returns:
            Answer to the user's doubt
        """
        return self.chain.invoke({
            "site": site,
            "title": title,
            "problem": problem,
            "question": question,
            "chat_history": chat_history
        })
