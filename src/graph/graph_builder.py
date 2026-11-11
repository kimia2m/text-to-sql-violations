"""Text-to-SQL LangGraph assembly."""

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.config import settings
from src.graph.nodes.text_to_sql import create_text_to_sql_node
from src.graph.state import TextToSQLState


def build_graph():
    """Build and compile the text-to-SQL graph."""
    model = ChatOpenAI(
        model=settings.model_config.model_name,
        base_url=settings.model_config.base_url,
        api_key=settings.model_config.api_key,
        temperature=settings.model_config.temperature,
        max_tokens=settings.model_config.max_tokens,
        timeout=settings.model_config.timeout_seconds,
        max_retries=settings.model_config.max_retries,
    )

    graph = StateGraph(TextToSQLState)
    graph.add_node("generate_sql", create_text_to_sql_node(model))
    graph.add_edge(START, "generate_sql")
    graph.add_edge("generate_sql", END)
    return graph.compile()

