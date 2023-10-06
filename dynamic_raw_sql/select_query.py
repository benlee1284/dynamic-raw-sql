from collections.abc import Iterable
from typing import Any, Literal, Self


class SelectQuery:
    def __init__(
        self,
        from_table: str = None,
        select_elements: Iterable[Literal] = None,
        where_conditions: Iterable[str] = None,
    ) -> None:
        self.__from_table = from_table

        if select_elements is None:
            self.__select_elements = []
        elif (
            isinstance(select_elements, Iterable)
            and not isinstance(select_elements, str)
        ):
            self.__select_elements = list(select_elements)
        else:
            raise TypeError()

        if where_conditions is None:
            self.__where_conditions = []
        elif (
            isinstance(where_conditions, Iterable)
            and not isinstance(where_conditions, str)
        ):
            self.__where_conditions = list(where_conditions)
        else:
            raise TypeError()

    def from_(self, table: str) -> Self:
        self.__from_table = table
        return self

    def select(self, *statements: Any) -> Self:
        if isinstance(statements, Iterable) and not isinstance(statements, str):
            self.__select_elements += list(statements)
        else:
            self.__select_elements += [statements]
        return self

    def where(self, *conditions: str) -> Self:
        if isinstance(conditions, Iterable) and not isinstance(conditions, str):
            self.__where_conditions += list(conditions)
        else:
            self.__where_conditions += [conditions]
        return self

    def build(self) -> str:
        "Build SQL query string"
        query_string = f"SELECT {', '.join(str(x) for x in self.__select_elements)}"
        if self.__from_table is not None:
            query_string += f" FROM {self.__from_table}"

        if self.__where_conditions:
            query_string += f" WHERE {' AND '.join(self.__where_conditions)}"

        return query_string
