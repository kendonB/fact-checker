"""LLM model helpers for claim filtering."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

from claim_filter.llm.config import MODEL_NAME, DEFAULT_TEMPERATURE

# Default LLM instance
openai_llm = init_chat_model(model=MODEL_NAME, temperature=DEFAULT_TEMPERATURE)


def get_llm() -> BaseChatModel:
    """Return a new LLM instance with default settings."""
    return init_chat_model(model=MODEL_NAME, temperature=DEFAULT_TEMPERATURE)
