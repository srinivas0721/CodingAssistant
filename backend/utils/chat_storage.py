from typing import List, Dict
import hashlib
from dataclasses import dataclass
from datetime import datetime
from collections import deque

@dataclass
class ChatMessage:
    """Stores a single message with metadata."""
    role: str  # 'user' or 'assistant'
    content: str
    agent_used: str
    timestamp: str

class ChatHistoryStorage:
    """Stores chat history with a maximum of 15 messages per problem."""
    def __init__(self, max_messages: int = 15):
        self._storage: Dict[str, deque] = {}
        self.max_messages = max_messages
    
    def _generate_key(self, site: str, problem_title: str) -> str:
        """Generate a unique key for a problem based on site and title."""
        unique_str = f"{site}:{problem_title}"
        return hashlib.md5(unique_str.encode()).hexdigest()
    
    def get_chat_history(self, site: str, problem_title: str) -> List[ChatMessage]:
        """Get the chat history for this problem (last 15 messages)."""
        key = self._generate_key(site, problem_title)
        if key in self._storage:
            return list(self._storage[key])
        return []
    
    def add_message(self, site: str, problem_title: str, role: str, content: str, agent_used: str = "") -> None:
        """Add a message to chat history (maintains last 15 messages)."""
        key = self._generate_key(site, problem_title)
        
        if key not in self._storage:
            self._storage[key] = deque(maxlen=self.max_messages)
        
        message = ChatMessage(
            role=role,
            content=content,
            agent_used=agent_used,
            timestamp=datetime.utcnow().isoformat()
        )
        
        self._storage[key].append(message)
    
    def format_history_for_prompt(self, site: str, problem_title: str) -> str:
        """Format chat history as a string for use in prompts."""
        history = self.get_chat_history(site, problem_title)
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history:
            if msg.role == "user":
                formatted.append(f"User: {msg.content}")
            else:
                agent_info = f" (via {msg.agent_used})" if msg.agent_used else ""
                formatted.append(f"Assistant{agent_info}: {msg.content}")
        
        return "\n\n".join(formatted)
    
    def clear_history(self, site: str, problem_title: str) -> None:
        """Clear chat history for a specific problem."""
        key = self._generate_key(site, problem_title)
        if key in self._storage:
            del self._storage[key]

chat_storage = ChatHistoryStorage()
