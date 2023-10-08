from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Prevent circular import
    from .select_query import SelectQuery


class UnionedQuery:
    __slots__ = (
        "__queries",
        "__union_all",
    )

    def __init__(
        self,
        queries: Iterable["SelectQuery"],
        union_all: bool = False,
    ) -> None:
        self.__queries = queries
        self.__union_all = union_all

    def build(self) -> str:
        union_type = "UNION ALL" if self.__union_all else "UNION"

        query_body = f") {union_type} (".join(
            query.build() for query in self.__queries
        )
        return f"({query_body})"
