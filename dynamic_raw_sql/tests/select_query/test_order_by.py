from collections.abc import Iterable
import pytest
from typing import Any

from dynamic_raw_sql import SelectQuery


@pytest.mark.parametrize(
    "order_by_clauses, expected_query",
    [
        pytest.param(None, "SELECT ", id="none"),
        pytest.param(["column_1"], "SELECT  ORDER BY column_1", id="singular_clause"),
        pytest.param(
            ["column_1", "1"], "SELECT  ORDER BY column_1, 1", id="multiple_clauses"
        ),
        pytest.param(["column_1", 1], "SELECT  ORDER BY column_1, 1", id="mixed_types"),
    ],
)
def test_instantiate_query_with_orderby_clause(
    order_by_clauses: Iterable[Any], expected_query: str
) -> None:
    query = SelectQuery(order_by_elements=order_by_clauses)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "order_by_clauses, expected_query",
    [
        pytest.param(["column_1"], "SELECT  ORDER BY column_1", id="singular_clause"),
        pytest.param(
            ["column_1", "1"], "SELECT  ORDER BY column_1, 1", id="multiple_clauses"
        ),
        pytest.param(["column_1", 1], "SELECT  ORDER BY column_1, 1", id="mixed_types"),
    ],
)
def test_add_order_by_clauses_to_empty_query(
    order_by_clauses: Iterable[Any], expected_query: str
) -> None:
    query = SelectQuery().order_by(*order_by_clauses)
    assert query.build() == expected_query


def test_add_order_by_clauses_iteratively() -> None:
    query = SelectQuery().order_by(1)
    query = query.order_by("column_1")
    assert query.build() == "SELECT  ORDER BY 1, column_1"


@pytest.mark.parametrize(
    "order_by_clauses",
    [
        pytest.param(1, id="int"),
        pytest.param("1", id="str"),
        pytest.param(3.14, id="float"),
    ],
)
def test_instantiating_query_with_non_iterable_orderby_clause_raises_error(
    order_by_clauses: Any,
) -> None:
    with pytest.raises(TypeError):
        SelectQuery(order_by_elements=order_by_clauses)
