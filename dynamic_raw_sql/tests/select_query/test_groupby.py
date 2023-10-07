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
    query = SelectQuery(group_by=group_by_clauses)
    assert query.build() == expected_query
