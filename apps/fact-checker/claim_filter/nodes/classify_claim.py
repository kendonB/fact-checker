"""Node that classifies a claim into a certainty category."""

import logging
from typing import Dict

from pydantic import BaseModel, Field

from claim_filter.llm import get_llm
from claim_filter.schemas import ClaimCategory, ClaimFilterState
from utils.llm import call_llm_with_structured_output

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You categorize factual claims based on how likely they are to be true.\nReturn only the category name."""

HUMAN_PROMPT = "Claim: \"{claim}\""


class ClassificationOutput(BaseModel):
    """Structured output for the classification LLM call."""

    category: ClaimCategory = Field(description="Chosen category")


async def classify_claim_node(state: ClaimFilterState) -> Dict[str, ClaimCategory]:
    """Classify a claim using an LLM."""

    claim = state.claim
    llm = get_llm()

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT.format(claim=claim)),
    ]

    response = await call_llm_with_structured_output(
        llm=llm,
        output_class=ClassificationOutput,
        messages=messages,
        context_desc=f"claim classification for '{claim}'",
    )

    if not response:
        logger.warning("LLM failed to classify claim, defaulting to UNSURE")
        return {"category": ClaimCategory.UNSURE}

    return {"category": response.category}
