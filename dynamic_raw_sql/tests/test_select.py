from collections.abc import Iterable
import pytest

from ..select_query import SelectQuery


@pytest.mark.parametrize(
    "statements, expected_query",
    [
        pytest.param(
            ["*"],
            "SELECT *",
            id="singular_statement"
        ),
        pytest.param(
            ["1, 2, 3"],
            "SELECT 1, 2, 3",
            id="multiple_statements"
        ),
    ],
)
def test_add_select_statements_to_empty_query(
    statements: str | Iterable[str], expected_query: str
) -> None:
    query = SelectQuery()
    query = query.select(*statements)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "statements, expected_query",
    [
        pytest.param(
            ["SUM(column_3)"],
            "SELECT column, other_column, SUM(column_3)",
            id="singular_statement"
        ),
        pytest.param(
            ["SUM(column_3)", "column_4"],
            "SELECT column, other_column, SUM(column_3), column_4",
            id="multiple_statements"
        ),
    ],
)
def test_add_select_statements_to_existing_query(
    statements: Iterable[str], expected_query: str
) -> None:
    query = SelectQuery(select_elements=["column", "other_column"])
    query = query.select(*statements)
    print(query.__dict__)
    assert query.build() == expected_query


@pytest.mark.parametrize(
    "statements, expected_query",
    [
        pytest.param(
            ["*"],
            "SELECT *",
            id="singular_select"
        ),
        pytest.param(
            ["%s"],
            "SELECT %s",
            id="select_with_parameter"
        ),
        pytest.param(
            ["'USD'"],
            "SELECT 'USD'",
            id="select_constant"
        ),
        pytest.param(
            [1, "2", 3.14, (12, 44)],
            "SELECT 1, 2, 3.14, (12, 44)",
            id="multiple_selects_list_variate_types"
        ),
        pytest.param(
            ["1", "2", "3"],
            "SELECT 1, 2, 3",
            id="multiple_selects_list"
        ),
        pytest.param(
            ("1", "2", "3"),
            "SELECT 1, 2, 3",
            id="multiple_selects_tuple"
        ),
        pytest.param(
            # Use dict for set-like behaviour because sets are unordered so this test
            # would fail intermittently if using a set
            {"1": None, "2": None, "3": None},
            "SELECT 1, 2, 3",
            id="multiple_selects_set"
        ),
    ],
)
def test_instantiate_with_select_statements(
    statements: Iterable[str], expected_query: str
) -> None:
    query = SelectQuery(select_elements=statements)
    assert query.build() == expected_query


def test_instantiating_with_invalid_select_raises_error() -> None:
    with pytest.raises(TypeError):
        SelectQuery(select_elements="*")

    with pytest.raises(TypeError):
        SelectQuery(select_elements=11)


def test_instantiate_query_with_from_clause() -> None:
    query = SelectQuery(from_table="table")

    assert query.build() == "SELECT  FROM table"


def test_add_from_clause_to_empty_query() -> None:
    query = SelectQuery().from_("table")

    assert query.build() == "SELECT  FROM table"


def test_add_from_clause_to_existing_query() -> None:
    query = SelectQuery(
        select_elements=["column_1", "column_2", "SUM(column_3)"]
    ).from_("table")

    assert query.build() == "SELECT column_1, column_2, SUM(column_3) FROM table"


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(
            ["1=1"],
            "SELECT  WHERE 1=1",
            id="singular_condition"
        ),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  WHERE 1=1 AND column_1=42",
            id="multiple_conditions"
        ),
        pytest.param(
            ["column_1=%s"],
            "SELECT  WHERE column_1=%s",
            id="condition_with_parameter"
        ),
    ],
)
def test_add_where_clause_to_empty_query(conditions: list[str], expected_query: str) -> None:
    query = SelectQuery().where(*conditions)

    assert query.build() == expected_query


@pytest.mark.parametrize(
    "conditions, expected_query",
    [
        pytest.param(
            ["1=1"],
            "SELECT  WHERE 1=1",
            id="singular_condition"
        ),
        pytest.param(
            ["1=1", "column_1=42"],
            "SELECT  WHERE 1=1 AND column_1=42",
            id="multiple_conditions"
        ),
        pytest.param(
            ["column_1=%s"],
            "SELECT  WHERE column_1=%s",
            id="condition_with_parameter"
        ),
    ],
)
def test_instantiate_query_with_where_conditions(
    conditions: list[str], expected_query: str
) -> None:
    query = SelectQuery(where_conditions=conditions)

    assert query.build() == expected_query
def test_instantiating_with_invalid_where_condition_raises_error() -> None:
    with pytest.raises(TypeError):
        SelectQuery(where_conditions="1=1")

    with pytest.raises(TypeError):
        SelectQuery(where_conditions=1)
