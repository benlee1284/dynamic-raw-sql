import pytest
from typing import Any

from dynamic_raw_sql import SelectQuery


def test_instantiate_query_with_join_clause() -> None:
    query = SelectQuery(
        joins=[
            "INNER JOIN table2 ON 1=1",
            "LEFT OUTER JOIN table3 ON column_1=column_2",
        ]
    )

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


@pytest.mark.parametrize(
    "joins, expected_query",
    [
        pytest.param(
            ["INNER JOIN table2 ON 1=1"],
            "SELECT  INNER JOIN table2 ON 1=1",
            id="single_join",
        ),
        pytest.param(
            ["INNER JOIN table2 ON 1=1", "LEFT OUTER JOIN table3 ON column_1=column_2"],
            "SELECT  INNER JOIN table2 ON 1=1 "
            "LEFT OUTER JOIN table3 ON column_1=column_2",
            id="two_joins",
        ),
    ],
)
def test_add_join_clauses_to_empty_query(joins: list[str], expected_query: str) -> None:
    query = SelectQuery().join(*joins)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "joins, expected_query",
    [
        pytest.param(
            ["INNER JOIN table2 ON 1=1"],
            "SELECT * FROM table INNER JOIN table2 ON 1=1",
            id="single_join",
        ),
        pytest.param(
            ["INNER JOIN table2 ON 1=1", "LEFT OUTER JOIN table3 ON column_1=column_2"],
            "SELECT * FROM table INNER JOIN table2 ON 1=1 "
            "LEFT OUTER JOIN table3 ON column_1=column_2",
            id="two_joins",
        ),
    ],
)
def test_add_join_clauses_to_existing_query(
    joins: list[str], expected_query: str
) -> None:
    query = SelectQuery(
        select_elements=["*"],
        from_table="table",
    ).join(*joins)
    assert query.build() == expected_query


def test_add_join_clauses_iteratively() -> None:
    query = SelectQuery(
        select_elements=["*"],
        from_table="table",
    )
    query = query.join("INNER JOIN table2 ON 1=1")
    query = query.join("LEFT OUTER JOIN table3 ON column_1=column_2")
    assert (
        query.build() == "SELECT * FROM table "
        "INNER JOIN table2 ON 1=1 "
        "LEFT OUTER JOIN table3 ON column_1=column_2"
    )
