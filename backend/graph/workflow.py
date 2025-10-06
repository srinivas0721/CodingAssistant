from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agents.intent_classifier import IntentClassifier
from agents.explain_agent import ExplainAgent
from agents.debug_agent import DebugAgent
from agents.suggest_agent import SuggestAgent

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

class CPAssistantGraph:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.explain_agent = ExplainAgent()
        self.debug_agent = DebugAgent()
        self.suggest_agent = SuggestAgent()
        
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
    
    def _route_by_intent(self, state: GraphState) -> Literal["explain", "debug", "suggest"]:
        intent = state["intent"]
        if intent in ["explain", "debug", "suggest"]:
            return intent  # type: ignore
        return "explain"
    
    def _build_graph(self):
        workflow = StateGraph(GraphState)
        
        workflow.add_node("classify", self._classify_intent)
        workflow.add_node("explain", self._explain_node)
        workflow.add_node("debug", self._debug_node)
        workflow.add_node("suggest", self._suggest_node)
        
        workflow.set_entry_point("classify")
        
        workflow.add_conditional_edges(
            "classify",
            self._route_by_intent,
            {
                "explain": "explain",
                "debug": "debug",
                "suggest": "suggest"
            }
        )
        
        workflow.add_edge("explain", END)
        workflow.add_edge("debug", END)
        workflow.add_edge("suggest", END)
        
        return workflow.compile()
    
    def run(self, input_data: dict) -> dict:
        result = self.graph.invoke(input_data)
        return result
