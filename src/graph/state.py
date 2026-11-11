from typing_extensions import NotRequired, TypedDict


class TextToSQLState(TypedDict):
    """State flowing through the text-to-SQL graph."""

    query: str
    schema: NotRequired[str]
    sql: NotRequired[str]

