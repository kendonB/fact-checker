import logging

from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from claim_filter.nodes import classify_claim_node
from claim_filter.schemas import ClaimFilterState

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_graph() -> CompiledStateGraph:
    """Create the claim filter workflow graph."""
    workflow = StateGraph(ClaimFilterState)

    workflow.add_node("classify_claim_node", classify_claim_node)
    workflow.set_entry_point("classify_claim_node")
    workflow.set_finish_point("classify_claim_node")

    return workflow.compile()


graph = create_graph()
