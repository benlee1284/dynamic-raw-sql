import pytest
from typing import Any

from dynamic_raw_sql import SelectQuery


def test_instantiate_query_with_join_clause() -> None:
    query = SelectQuery(joins=[
        "INNER JOIN table2 ON 1=1",
        "LEFT OUTER JOIN table3 ON column_1=column_2",
    ])

    assert (
        query.build() == "SELECT  INNER JOIN table2 ON 1=1 "
        "LEFT OUTER JOIN table3 ON column_1=column_2"
    )


@pytest.mark.parametrize(
    "joins",
    [
        pytest.param("INNER JOIN table2 ON 1=1", id="string"),
        pytest.param(1, id="int"),
        pytest.param([1, 2], id="list of ints"),
    ],
)
def test_instantiating_query_with_invalid_join_clause_erros(joins: Any) -> None:
    with pytest.raises(TypeError):
        SelectQuery(joins=joins)
