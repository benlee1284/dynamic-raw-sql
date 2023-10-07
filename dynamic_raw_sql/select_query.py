from collections.abc import Iterable
from typing import Any, Literal, Self


class SelectQuery:
    __slots__ = (
        "__from_table",
        "__select_elements",
        "__where_conditions",
        "__group_by_elements",
    )

    __from_table: str
    __select_elements: list[Any]
    __where_conditions: list[str]
    __group_by_elements: list[Any]

    def __init__(
        self,
        from_table: str = None,
        select_elements: Iterable[Literal] = None,
        where_conditions: Iterable[str] = None,
        group_by_elements: Iterable[Any] = None,
    ) -> None:
        if isinstance(from_table, str) or from_table is None:
            self.__from_table = from_table
        else:
            raise TypeError(
                "From table must be of type str or None. "
                f"Type {type(from_table)} was given."
            )

        if select_elements is None:
            self.__select_elements = []
        elif isinstance(select_elements, Iterable) and not isinstance(
            select_elements, str
        ):
            self.__select_elements = list(select_elements)
        else:
            raise TypeError(
                "Param `select_elements` accepts only an iterable of literals. "
                f"Type {type(select_elements)} was given."
            )

        if where_conditions is None:
            self.__where_conditions = []
        elif (
            isinstance(where_conditions, Iterable)
            and not isinstance(where_conditions, str)
            and all(isinstance(condition, str) for condition in where_conditions)
        ):
            self.__where_conditions = list(where_conditions)
        else:
            raise TypeError(
                "Param `where_conditions` accepts only an iterable of string literals. "
                f"Type {type(select_elements)} was given."
            )

        if group_by_elements is None:
            self.__group_by_elements = []
        elif isinstance(group_by_elements, Iterable) and not isinstance(
            group_by_elements, str
        ):
            self.__group_by_elements = list(group_by_elements)
        else:
            raise TypeError(
                "Param `group_by_elements` accepts only an iterable of literals. "
                f"Type {type(group_by_elements)} was given."
            )

    def from_(self, table: str) -> Self:
        if isinstance(table, str):
            self.__from_table = table
            return self
        else:
            raise TypeError(
                f"From table must be of type string. Type {type(table)} was given."
            )

    def select(self, *statements: tuple[Any]) -> Self:
        self.__select_elements += list(statements)
        return self

    def where(self, *conditions: tuple[str]) -> Self:
        if not all(isinstance(condition, str) for condition in conditions):
            raise TypeError("Where conditions must all be of type string.")
        self.__where_conditions += list(conditions)
        return self

    def group_by(self, *statements: tuple[Any]) -> Self:
        self.__group_by_elements += list(statements)
        return self

    def build(self) -> str:
        "Build SQL query string"
        query_string = f"SELECT {', '.join(str(x) for x in self.__select_elements)}"
        if self.__from_table is not None:
            query_string += f" FROM {self.__from_table}"

        if self.__where_conditions:
            query_string += f" WHERE {' AND '.join(self.__where_conditions)}"

        if self.__group_by_elements:
            query_string += (
                f" GROUP BY {', '.join(str(x) for x in self.__group_by_elements)}"
            )

        return query_string
