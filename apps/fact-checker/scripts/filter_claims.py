import argparse
import asyncio
import csv
import json
from pathlib import Path
from typing import Iterable, List

from claim_filter import graph as claim_filter_graph
from claim_filter.schemas import ClaimCategory


def read_claims(path: Path) -> List[str]:
    if path.suffix.lower() == ".json":
        with path.open() as f:
            return json.load(f)
    if path.suffix.lower() == ".csv":
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            field = "claim" if "claim" in reader.fieldnames else reader.fieldnames[0]
            return [row[field] for row in reader]
    with path.open() as f:
        return [line.strip() for line in f if line.strip()]


def write_claims(path: Path, claims: Iterable[str]) -> None:
    if path.suffix.lower() == ".json":
        with path.open("w") as f:
            json.dump(list(claims), f, indent=2)
        return
    if path.suffix.lower() == ".csv":
        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["claim"])
            for claim in claims:
                writer.writerow([claim])
        return
    with path.open("w") as f:
        for claim in claims:
            f.write(claim + "\n")


async def classify(claims: Iterable[str]) -> List[ClaimCategory]:
    results = []
    for claim in claims:
        result = await claim_filter_graph.ainvoke({"claim": claim})
        results.append(result.get("category"))
    return results


def parse_keep(value: str) -> List[ClaimCategory]:
    parts = [v.strip() for v in value.split(",") if v.strip()]
    return [ClaimCategory[p] for p in parts]


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify and filter claims")
    parser.add_argument("input_file", type=Path)
    parser.add_argument("output_file", type=Path)
    parser.add_argument(
        "--keep",
        required=True,
        help="Comma-separated list of categories to keep",
    )
    args = parser.parse_args()

    claims = read_claims(args.input_file)
    keep_categories = parse_keep(args.keep)

    categories = asyncio.run(classify(claims))

    kept = [claim for claim, cat in zip(claims, categories) if cat in keep_categories]

    write_claims(args.output_file, kept)


if __name__ == "__main__":
    main()
