"""Command-line entry point for batch text-to-SQL generation."""

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from src.graph.graph_builder import build_graph
from src.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_INPUT_PATH = Path(__file__).parent.parent / "data" / "queries.json"
DEFAULT_SCHEMA_PATH = Path(__file__).parent.parent / "data" / "schema.sql"


def _load_queries(path: Path) -> list[dict[str, Any]]:
    """Load the `queries` array; every record needs an `id` and a `prompt`."""
    with path.open(encoding="utf-8") as input_file:
        queries = json.load(input_file)["queries"]
    for index, record in enumerate(queries):
        if not isinstance(record.get("id"), str) or not isinstance(record.get("prompt"), str):
            raise ValueError(f"Query at index {index} needs string `id` and `prompt` fields")
    return queries


def _load_schema(path: Path) -> str:
    """Load the shared database schema used in every prompt."""
    schema = path.read_text(encoding="utf-8").strip()
    if not schema:
        raise ValueError(f"Schema file is empty: {path}")
    return schema


async def generate_sql(input_path: Path, schema_path: Path) -> list[dict[str, Any]]:
    """Generate SQL for every query record in the input JSON."""
    queries = _load_queries(input_path)
    schema = _load_schema(schema_path)
    graph = build_graph()
    results = []

    for index, record in enumerate(queries, start=1):
        logger.info("Generating SQL for query %d/%d (%s)", index, len(queries), record["id"])
        state = await graph.ainvoke({"query": record["prompt"], "schema": schema})
        results.append({"id": record["id"], "prompt": record["prompt"], "sql": state["sql"]})

    return results


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate SQL from JSON queries")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=DEFAULT_INPUT_PATH,
        help=f"JSON file containing natural-language queries (default: {DEFAULT_INPUT_PATH})",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA_PATH,
        help=f"SQL DDL schema file (default: {DEFAULT_SCHEMA_PATH})",
    )
    parser.add_argument(
        "-o", "--output", type=Path, help="Optional JSON file for generated SQL results"
    )
    return parser.parse_args()


async def main() -> None:
    args = _parse_args()
    results = await generate_sql(args.input, args.schema)
    output = json.dumps(results, indent=2, ensure_ascii=False)

    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
        logger.info("Wrote %d SQL queries to %s", len(results), args.output)
    else:
        print(output)


if __name__ == "__main__":
    asyncio.run(main())
