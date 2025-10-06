from typing import List, Dict
import hashlib
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HintEntry:
    """Stores a single hint with metadata."""
    hint_number: int
    hint_text: str
    timestamp: str

class HintHistoryStorage:
    def __init__(self):
        self._storage: Dict[str, List[HintEntry]] = {}
    
    def _generate_key(self, site: str, problem_title: str) -> str:
        """Generate a unique key for a problem based on site and title."""
        unique_str = f"{site}:{problem_title}"
        return hashlib.md5(unique_str.encode()).hexdigest()
    
    def get_hint_history(self, site: str, problem_title: str) -> List[HintEntry]:
        """Get the list of hints already given for this problem."""
        key = self._generate_key(site, problem_title)
        return self._storage.get(key, [])
    
    def add_hint(self, site: str, problem_title: str, hint_number: int, hint_text: str) -> None:
        """Record a hint that has been given for this problem."""
        key = self._generate_key(site, problem_title)
        if key not in self._storage:
            self._storage[key] = []
        
        entry = HintEntry(
            hint_number=hint_number,
            hint_text=hint_text,
            timestamp=datetime.utcnow().isoformat()
        )
        
        existing_numbers = [h.hint_number for h in self._storage[key]]
        if hint_number not in existing_numbers:
            self._storage[key].append(entry)
            self._storage[key].sort(key=lambda x: x.hint_number)
    
    def reset_history(self, site: str, problem_title: str) -> None:
        """Clear hint history for a specific problem."""
        key = self._generate_key(site, problem_title)
        if key in self._storage:
            del self._storage[key]
    
    def get_next_hint_number(self, site: str, problem_title: str) -> int:
        """Get the next hint number to give (1-indexed)."""
        history = self.get_hint_history(site, problem_title)
        if not history:
            return 1
        return max(h.hint_number for h in history) + 1

hint_storage = HintHistoryStorage()
