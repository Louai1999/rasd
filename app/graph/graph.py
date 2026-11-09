"""The ticket graph, up to the point where the request reaches the insurer.

The second half (insurer reply, payment gate, issuing) is added in later phases.
"""

from datetime import date

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.domain import TicketStatus
from app.graph import nodes
from app.graph.state import TicketState
from app.integrations.channels import InsurerChannel


def _after_classify(state: TicketState) -> str:
    return "end" if state["status"] == TicketStatus.ESCALATED.value else "check_documents"


def _after_check(state: TicketState) -> str:
    return "request_documents" if state["issues"] else "draft_request"


def _after_approval(state: TicketState) -> str:
    return "end" if state.get("status") == TicketStatus.REJECTED.value else "send_to_insurer"


def build_graph(channel: InsurerChannel, *, checkpointer=None, today_fn=date.today):
    g = StateGraph(TicketState)
    g.add_node("classify", nodes.classify)
    g.add_node("check_documents", nodes.make_check_documents(today_fn))
    g.add_node("request_documents", nodes.request_documents)
    g.add_node("draft_request", nodes.draft_request)
    g.add_node("staff_approval", nodes.staff_approval)
    g.add_node("send_to_insurer", nodes.make_send_to_insurer(channel))

    g.add_edge(START, "classify")
    g.add_conditional_edges(
        "classify", _after_classify, {"end": END, "check_documents": "check_documents"}
    )
    g.add_conditional_edges(
        "check_documents",
        _after_check,
        {"request_documents": "request_documents", "draft_request": "draft_request"},
    )
    # The ticket waits for the customer; new documents start a fresh run.
    g.add_edge("request_documents", END)
    g.add_edge("draft_request", "staff_approval")
    g.add_conditional_edges(
        "staff_approval", _after_approval, {"end": END, "send_to_insurer": "send_to_insurer"}
    )
    g.add_edge("send_to_insurer", END)

    return g.compile(checkpointer=checkpointer or InMemorySaver())
