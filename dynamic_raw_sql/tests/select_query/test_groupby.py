from collections.abc import Iterable
import pytest
from typing import Any

from dynamic_raw_sql import SelectQuery


@pytest.mark.parametrize(
    "group_by_clauses, expected_query",
    [
        pytest.param(None, "SELECT ", id="none"),
        pytest.param(["column_1"], "SELECT GROUP BY column_1", id="singular_clause"),
        pytest.param(
            ["column_1", "1"], "SELECT GROUP BY column_1, 1", id="multiple_clauses"
        ),
        pytest.param(["column_1", 1], "SELECT GROUP BY column_1, 1", id="mixed_types"),
    ],
)
def test_instantiate_query_with_groupby_clause(
    group_by_clauses: Iterable[Any], expected_query: str
) -> None:
    query = SelectQuery(group_by_elements=group_by_clauses)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "group_by_clauses, expected_query",
    [
        pytest.param(["column_1"], "SELECT GROUP BY column_1", id="singular_clause"),
        pytest.param(
            ["column_1", "1"], "SELECT GROUP BY column_1, 1", id="multiple_clauses"
        ),
        pytest.param(["column_1", 1], "SELECT GROUP BY column_1, 1", id="mixed_types"),
    ],
)
def test_add_group_by_clauses_to_empty_query(
    group_by_clauses: Iterable[Any], expected_query: str
) -> None:
    query = SelectQuery().group_by(*group_by_clauses)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "group_by_clauses",
    [
        pytest.param(1, id="int"),
        pytest.param("1", id="str"),
        pytest.param(3.14, id="float"),
    ],
)
def test_instantiating_query_with_non_iterable_groupby_clause_raises_error(
    group_by_clauses: Any,
) -> None:
    with pytest.raises(TypeError):
        SelectQuery(group_by_elements=group_by_clauses)
