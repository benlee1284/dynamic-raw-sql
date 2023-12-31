from collections.abc import Iterable
from typing import Any
import pytest

from dynamic_raw_sql import SelectQuery


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(["1=1"], "SELECT  WHERE 1=1", id="singular_condition"),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  WHERE 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"], "SELECT  WHERE column_1=%s", id="condition_with_parameter"
        ),
    ],
)
def test_add_where_clause_to_empty_query(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery().where(*conditions)

    assert query.build() == expected_query


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(["1=1"], "SELECT  WHERE 1=1", id="singular_condition"),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  WHERE 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"], "SELECT  WHERE column_1=%s", id="condition_with_parameter"
        ),
    ],
)
def test_instantiate_query_with_where_conditions(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery(where_conditions=conditions)

    assert query.build() == expected_query


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(
            ["1=1"],
            "SELECT * FROM table WHERE date='2012-12-12' AND 1=1",
            id="singular_condition",
        ),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT * FROM table WHERE date='2012-12-12' AND 1=1 AND column_1=42",
            id="multiple_conditions",
        ),
        pytest.param(
            ["column_1=%s"],
            "SELECT * FROM table WHERE date='2012-12-12' AND column_1=%s",
            id="condition_with_parameter",
        ),
    ],
)
def test_add_where_condition_to_existing_query(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery(
        from_table="table",
        select_elements=["*"],
        where_conditions=["date='2012-12-12'"],
    ).where(*conditions)

    assert query.build() == expected_query


def test_add_where_conditions_iteratively_to_existing_query() -> None:
    query = SelectQuery(
        from_table="table",
        select_elements=["*"],
        where_conditions=["date='2012-12-12'"],
    )
    query = query.where("1=1")
    query = query.where("column_1=42")

    assert (
        query.build()
        == "SELECT * FROM table WHERE date='2012-12-12' AND 1=1 AND column_1=42"
    )


@pytest.mark.parametrize(
    "conditions",
    [
        pytest.param("1=1", id="string"),
        pytest.param(1, id="int"),
        pytest.param([1, 23], id="list of non-strings"),
    ],
)
def test_instantiating_with_invalid_where_condition_raises_error(
    conditions: Any,
) -> None:
    with pytest.raises(TypeError):
        SelectQuery(where_conditions=conditions)


@pytest.mark.parametrize(
    "conditions",
    [
        pytest.param([1], id="singular non-string"),
        pytest.param([1, 23], id="series of non-strings"),
    ],
)
def test_adding_invalid_where_condition_raises_error(conditions: Iterable[Any]) -> None:
    with pytest.raises(TypeError):
        SelectQuery().where(*conditions)
