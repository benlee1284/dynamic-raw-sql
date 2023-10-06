from collections.abc import Iterable
from typing import Self


class SelectQuery:
    def __init__(
        self,
        from_table: str = None,
        select_elements: Iterable[str] = None,
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

    def from_(self, table: str) -> Self:
        return self.__class__(
            from_table=table,
            select_elements=self.__select_elements,
        )

    def select(self, *statements: any) -> Self:
        if isinstance(statements, Iterable) and not isinstance(statements, str):
            return self.__class__(
                select_elements=self.__select_elements + list(statements),
            )
        else:
            return self.__class__(
                select_elements=self.__select_elements + [statements],
            )

    def build(self) -> str:
        """Build SQL query string"""
        query_string = f"SELECT {', '.join(self.__select_elements)}"
        if self.__from_table is not None:
            query_string += f" FROM {self.__from_table}"

        return query_string
