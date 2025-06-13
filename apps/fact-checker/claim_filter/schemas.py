"""Data models for the claim filter."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ClaimCategory(str, Enum):
    """Categories used to label claims by certainty."""

    CERTAIN_TRUE = "CERTAIN_TRUE"
    PROBABLY_TRUE = "PROBABLY_TRUE"
    UNSURE = "UNSURE"
    PROBABLY_FALSE = "PROBABLY_FALSE"
    CERTAIN_FALSE = "CERTAIN_FALSE"


class CategorizedClaim(BaseModel):
    """A claim with its assigned category."""

    claim: str = Field(description="The claim text")
    category: ClaimCategory = Field(description="Assigned category")


class ClaimFilterState(BaseModel):
    """State object for the claim filter graph."""

    claim: str = Field(description="Claim to categorize")
    category: Optional[ClaimCategory] = Field(
        default=None, description="Resulting category after classification"
    )
