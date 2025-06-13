# Claim Filter

This module provides a lightweight agent that classifies individual claims by how certain they appear to be.
It can be used as a standalone component to quickly filter large sets of claims before running the heavier
fact‑checking pipeline.

## Categories

Claims are sorted into five certainty levels:

1. **CERTAIN_TRUE** – Very strong evidence the claim is true.
2. **PROBABLY_TRUE** – Likely true but not absolutely certain.
3. **UNSURE** – Not enough information to judge either way.
4. **PROBABLY_FALSE** – Likely false or misleading.
5. **CERTAIN_FALSE** – Clearly false based on known information.

## CLI Usage

A helper script `filter_claims.py` is provided. It classifies each claim from an input file and outputs only the
claims whose category matches the provided `--keep` values.

```bash
poetry run filter-claims input.json output.json --keep CERTAIN_TRUE,PROBABLY_TRUE
```

The input can be a JSON array, a CSV file with a `claim` column, or a plain text file with one claim per line.
The output is written in the same format as the input.
