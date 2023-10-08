from collections.abc import Iterable
from typing import Any
import pytest

from dynamic_raw_sql import SelectQuery


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(["1=1"], "SELECT  HAVING 1=1", id="singular_condition"),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  HAVING 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"], "SELECT  HAVING column_1=%s", id="condition_with_parameter"
        ),
    ],
)
def test_add_having_clause_to_empty_query(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery().having(*conditions)

    assert query.build() == expected_query


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(["1=1"], "SELECT  HAVING 1=1", id="singular_condition"),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  HAVING 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"], "SELECT  HAVING column_1=%s", id="condition_with_parameter"
        ),
    ],
)
def test_instantiate_query_with_having_conditions(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery(having_conditions=conditions)

    assert query.build() == expected_query


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(
            ["1=1"],
            "SELECT * FROM table HAVING date='2012-12-12' AND 1=1",
            id="singular_condition",
        ),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT * FROM table HAVING date='2012-12-12' AND 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"],
            "SELECT * FROM table HAVING date='2012-12-12' AND column_1=%s",
            id="condition_with_parameter",
        ),
    ],
)
def test_add_having_condition_to_existing_query(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery(
        from_table="table",
        select_elements=["*"],
        having_conditions=["date='2012-12-12'"],
    ).having(*conditions)

    assert query.build() == expected_query


def test_add_having_conditions_iteratively_to_existing_query() -> None:
    query = SelectQuery(
        from_table="table",
        select_elements=["*"],
        having_conditions=["date='2012-12-12'"],
    )
    query = query.having("1=1")
    query = query.having("column_1=42")

    assert (
        query.build()
        == "SELECT * FROM table HAVING date='2012-12-12' AND 1=1 AND column_1=42"
    )


@pytest.mark.parametrize(
    "conditions",
    [
        pytest.param("1=1", id="string"),
        pytest.param(1, id="int"),
        pytest.param([1, 23], id="list of non-strings"),
    ],
)
def test_instantiating_with_invalid_having_condition_raises_error(
    conditions: Any,
) -> None:
    with pytest.raises(TypeError):
        SelectQuery(having_conditions=conditions)


@pytest.mark.parametrize(
    "conditions",
    [
        pytest.param([1], id="singular non-string"),
        pytest.param([1, 23], id="series of non-strings"),
    ],
)
def test_adding_invalid_having_condition_raises_error(conditions: Iterable[Any]) -> None:
    with pytest.raises(TypeError):
        SelectQuery().having(*conditions)
