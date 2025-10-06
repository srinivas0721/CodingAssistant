from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agents.intent_classifier import IntentClassifier
from agents.explain_agent import ExplainAgent
from agents.debug_agent import DebugAgent
from agents.suggest_agent import SuggestAgent
from agents.solver_agent import SolverAgent
from agents.hint_agent import HintAgent
from utils.hint_storage import hint_storage

class GraphState(TypedDict):
    site: str
    problem_title: str
    problem_statement: str
    user_code: str
    language: str
    question: str
    intent: str
    answer: str
    agent_used: str
    preferred_language: str
    hint_steps: list

class CPAssistantGraph:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.explain_agent = ExplainAgent()
        self.debug_agent = DebugAgent()
        self.suggest_agent = SuggestAgent()
        self.solver_agent = SolverAgent()
        self.hint_agent = HintAgent()
        
        self.graph = self._build_graph()
    
    def _classify_intent(self, state: GraphState) -> GraphState:
        has_code = bool(state.get("user_code"))
        intent = self.intent_classifier.classify(state["question"], has_code)
        state["intent"] = intent
        return state
    
    def _explain_node(self, state: GraphState) -> GraphState:
        answer = self.explain_agent.run(
            site=state["site"],
            title=state.get("problem_title", ""),
            problem=state.get("problem_statement", ""),
            question=state["question"]
        )
        state["answer"] = answer
        state["agent_used"] = "ExplainAgent"
        return state
    
    def _debug_node(self, state: GraphState) -> GraphState:
        answer = self.debug_agent.run(
            site=state["site"],
            problem=state.get("problem_statement", ""),
            code=state.get("user_code", ""),
            language=state.get("language", "unknown"),
            question=state["question"]
        )
        state["answer"] = answer
        state["agent_used"] = "DebugAgent"
        return state
    
    def _suggest_node(self, state: GraphState) -> GraphState:
        answer = self.suggest_agent.run(
            site=state["site"],
            title=state.get("problem_title", ""),
            problem=state.get("problem_statement", ""),
            question=state["question"]
        )
        state["answer"] = answer
        state["agent_used"] = "SuggestAgent"
        return state
    
    def _solve_node(self, state: GraphState) -> GraphState:
        preferred_lang = state.get("preferred_language", "cpp")
        answer = self.solver_agent.run(
            site=state["site"],
            title=state.get("problem_title", ""),
            problem=state.get("problem_statement", ""),
            language=preferred_lang,
            question=state["question"]
        )
        state["answer"] = answer
        state["agent_used"] = "SolverAgent"
        return state
    
    def _hint_node(self, state: GraphState) -> GraphState:
        site = state["site"]
        title = state.get("problem_title", "")
        
        hint_history = hint_storage.get_hint_history(site, title)
        next_hint_num = hint_storage.get_next_hint_number(site, title)
        
        answer = self.hint_agent.run(
            site=site,
            title=title,
            problem=state.get("problem_statement", ""),
            hint_number=next_hint_num,
            previous_hints=hint_history,
            question=state["question"]
        )
        
        hint_storage.add_hint(site, title, next_hint_num, answer)
        
        state["answer"] = answer
        state["agent_used"] = "HintAgent"
        state["hint_steps"] = [h.hint_number for h in hint_storage.get_hint_history(site, title)]
        return state
    
    def _route_by_intent(self, state: GraphState) -> Literal["explain", "debug", "suggest", "solve", "hint"]:
        intent = state["intent"]
        valid_intents = ["explain", "debug", "suggest", "solve", "hint"]
        if intent in valid_intents:
            return intent  # type: ignore
        return "explain"
    
    def _build_graph(self):
        workflow = StateGraph(GraphState)
        
        workflow.add_node("classify", self._classify_intent)
        workflow.add_node("explain", self._explain_node)
        workflow.add_node("debug", self._debug_node)
        workflow.add_node("suggest", self._suggest_node)
        workflow.add_node("solve", self._solve_node)
        workflow.add_node("hint", self._hint_node)
        
        workflow.set_entry_point("classify")
        
        workflow.add_conditional_edges(
            "classify",
            self._route_by_intent,
            {
                "explain": "explain",
                "debug": "debug",
                "suggest": "suggest",
                "solve": "solve",
                "hint": "hint"
            }
        )
        
        workflow.add_edge("explain", END)
        workflow.add_edge("debug", END)
        workflow.add_edge("suggest", END)
        workflow.add_edge("solve", END)
        workflow.add_edge("hint", END)
        
        return workflow.compile()
    
    def run(self, input_data: dict) -> dict:
        result = self.graph.invoke(input_data)
        return result
