from datetime import datetime, timezone
from typing import Any, Dict, TypedDict

from langgraph.graph import END, START, StateGraph

from ai_agents.risk_agent import risk_agent
from ai_agents.decision_agent import decision_agent


# ============================================================
# LANGGRAPH STATE
# ============================================================

class AgentState(TypedDict, total=False):
    risk_event: Any
    risk_assessment: Dict[str, Any]
    decision: Dict[str, Any]


class AgentOrchestrator:
    """
    LangGraph-based autonomous AI-agent workflow.

    Risk Event
        -> Risk Intelligence Agent
        -> Decision Agent
        -> Operational Decision
    """

    def __init__(self):
        self.name = "Energy Supply Chain LangGraph Orchestrator"

        self.workflow = self._build_workflow()

    # ========================================================
    # RISK INTELLIGENCE NODE
    # ========================================================

    def _risk_analysis_node(
        self,
        state: AgentState,
    ) -> Dict[str, Any]:

        risk_event = state["risk_event"]

        risk_assessment = risk_agent.analyze_risk(
            risk_event
        )

        return {
            "risk_assessment": risk_assessment
        }

    # ========================================================
    # AI DECISION NODE
    # ========================================================

    def _decision_node(
        self,
        state: AgentState,
    ) -> Dict[str, Any]:

        risk_assessment = state[
            "risk_assessment"
        ]

        decision = decision_agent.make_decision(
            risk_assessment
        )

        return {
            "decision": decision
        }

    # ========================================================
    # BUILD LANGGRAPH WORKFLOW
    # ========================================================

    def _build_workflow(self):

        graph = StateGraph(AgentState)

        graph.add_node(
            "risk_intelligence_agent",
            self._risk_analysis_node,
        )

        graph.add_node(
            "decision_agent",
            self._decision_node,
        )

        graph.add_edge(
            START,
            "risk_intelligence_agent",
        )

        graph.add_edge(
            "risk_intelligence_agent",
            "decision_agent",
        )

        graph.add_edge(
            "decision_agent",
            END,
        )

        return graph.compile()

    # ========================================================
    # RUN LANGGRAPH WORKFLOW
    # ========================================================

    def process_risk_event(
        self,
        risk_event,
    ):

        initial_state: AgentState = {
            "risk_event": risk_event
        }

        final_state = self.workflow.invoke(
            initial_state
        )

        return {
            "orchestrator": self.name,
            "workflow_engine": "LangGraph",
            "workflow_status": "Completed",
            "risk_assessment": final_state[
                "risk_assessment"
            ],
            "decision": final_state[
                "decision"
            ],
            "processed_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }


agent_orchestrator = AgentOrchestrator()