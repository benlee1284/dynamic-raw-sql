from collections.abc import Iterable
from typing import Any, Literal, Self


class SelectQuery:
    __slots__ = (
        "__from_table",
        "__select_elements",
        "__joins",
        "__where_conditions",
        "__group_by_elements",
        "__having_conditions",
        "__order_by_elements",
    )

    __from_table: str
    __select_elements: list[Any]
    __joins: list[str]
    __where_conditions: list[str]
    __group_by_elements: list[Any]
    __having_conditions: list[str]
    __order_by_elements: list[Any]

    def __init__(
        self,
        from_table: str = None,
        select_elements: Iterable[Literal] = None,
        joins: Iterable[str] = None,
        where_conditions: Iterable[str] = None,
        group_by_elements: Iterable[Any] = None,
        having_conditions: Iterable[str] = None,
        order_by_elements: Iterable[Any] = None,
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

        if joins is None:
            self.__joins = []
        elif (
            isinstance(joins, Iterable)
            and not isinstance(joins, str)
            and all(isinstance(join, str) for join in joins)
        ):
            self.__joins = list(joins)
        else:
            raise TypeError(
                "Param `where_conditions` accepts only an iterable of string literals. "
                f"Type {type(joins)} was given."
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

        if having_conditions is None:
            self.__having_conditions = []
        elif (
            isinstance(having_conditions, Iterable)
            and not isinstance(having_conditions, str)
            and all(isinstance(condition, str) for condition in having_conditions)
        ):
            self.__having_conditions = list(having_conditions)
        else:
            raise TypeError(
                "Param `having_conditions` accepts only an iterable of string literals. "
                f"Type {type(select_elements)} was given."
            )

        if order_by_elements is None:
            self.__order_by_elements = []
        elif isinstance(order_by_elements, Iterable) and not isinstance(
            order_by_elements, str
        ):
            self.__order_by_elements = list(order_by_elements)
        else:
            raise TypeError(
                "Param `order_by_elements` accepts only an iterable of literals. "
                f"Type {type(order_by_elements)} was given."
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

    def join(self, *statements: tuple[str]) -> Self:
        if not all(isinstance(statement, str) for statement in statements):
            raise TypeError("Joins must all be of type string.")
        self.__joins += list(statements)
        return self

    def where(self, *conditions: tuple[str]) -> Self:
        if not all(isinstance(condition, str) for condition in conditions):
            raise TypeError("Where conditions must all be of type string.")
        self.__where_conditions += list(conditions)
        return self

    def group_by(self, *statements: tuple[Any]) -> Self:
        self.__group_by_elements += list(statements)
        return self

    def having(self, *conditions: tuple[str]) -> Self:
        if not all(isinstance(condition, str) for condition in conditions):
            raise TypeError("Having conditions must all be of type string.")
        self.__having_conditions += list(conditions)
        return self

    def order_by(self, *statements: tuple[Any]) -> Self:
        self.__order_by_elements += list(statements)
        return self

    def build(self) -> str:
        "Build SQL query string"
        query_string = f"SELECT {', '.join(str(x) for x in self.__select_elements)}"
        if self.__from_table is not None:
            query_string += f" FROM {self.__from_table}"

        if self.__joins:
            query_string = " ".join([query_string] + self.__joins)

        if self.__where_conditions:
            query_string += f" WHERE {' AND '.join(self.__where_conditions)}"

        if self.__group_by_elements:
            query_string += (
                f" GROUP BY {', '.join(str(x) for x in self.__group_by_elements)}"
            )

        if self.__having_conditions:
            query_string += f" HAVING {' AND '.join(self.__having_conditions)}"

        if self.__order_by_elements:
            query_string += (
                f" ORDER BY {', '.join(str(x) for x in self.__order_by_elements)}"
            )

        return query_string
