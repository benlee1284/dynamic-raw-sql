from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Prevent circular import
    from .select_query import SelectQuery


class UnionedQuery:
    __slots__ = ("__queries",)

    def __init__(
        self,
        queries: Iterable["SelectQuery"],
    ) -> None:
        self.__queries = queries

    def build(self) -> str:
        query_body = ") UNION (".join(query.build() for query in self.__queries)
        return f"({query_body})"
