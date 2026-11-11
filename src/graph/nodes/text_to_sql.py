"""Node for converting a natural-language question into SQL."""

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.graph.state import TextToSQLState
from src.utils.logger import get_logger

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are a text-to-SQL translator.
Follow the user's prompt exactly and return only the requested SQLite query.
Do not add Markdown fences, explanations, or comments."""


def _content_to_text(content: Any) -> str:
    """Normalize the content returned by a chat model to plain text."""
    if isinstance(content, str):
        text = content.strip()
    elif isinstance(content, list):
        parts = [
            block["text"]
            for block in content
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        ]
        text = "".join(parts).strip()
    else:
        text = str(content).strip()

    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        return "\n".join(lines[1:-1]).strip()
    return text


def _to_single_line_sql(sql: str) -> str:
    """Collapse formatting whitespace without changing quoted SQL values."""
    output: list[str] = []
    in_quote: str | None = None
    pending_space = False
    index = 0

    sql = sql.strip()
    while index < len(sql):
        character = sql[index]
        if in_quote:
            output.append(character)
            if character == in_quote:
                if index + 1 < len(sql) and sql[index + 1] == in_quote:
                    output.append(sql[index + 1])
                    index += 1
                else:
                    in_quote = None
            index += 1
            continue

        if character in ("'", '"'):
            if pending_space and output:
                output.append(" ")
            pending_space = False
            output.append(character)
            in_quote = character
        elif character.isspace():
            pending_space = True
        else:
            if pending_space and output:
                output.append(" ")
            pending_space = False
            output.append(character)
        index += 1

    return "".join(output).strip()


def create_text_to_sql_node(model):
    """Create a graph node that generates SQL for one question."""

    def generate_sql(state: TextToSQLState) -> TextToSQLState:
        schema = state.get("schema", "").strip()
        prompt = f"""[Schema DDL]
{schema}

Definitions:
- DTI = existing_debt_sek / (salary_monthly_sek * 12)
- monthly payment = loan_amount_sek / loan_term_months (no interest)
- annual salary = salary_monthly_sek * 12
Write one SQL query (SQLite) that answers the request. Return only the query
on a single line, with no line breaks.

Request: {state["query"]}"""
        response = model.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
        )
        sql = _to_single_line_sql(_content_to_text(response.content))
        if not sql:
            raise ValueError("The model returned an empty SQL query")

        logger.info("Generated SQL for query: %s", state["query"])
        return {**state, "sql": sql}

    return generate_sql
