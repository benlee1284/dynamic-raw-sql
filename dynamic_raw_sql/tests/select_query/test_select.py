from collections.abc import Iterable
import pytest

from dynamic_raw_sql import SelectQuery


@pytest.mark.parametrize(
    "statements, expected_query",
    [
        pytest.param(["*"], "SELECT *", id="singular_statement"),
        pytest.param(["1, 2, 3"], "SELECT 1, 2, 3", id="multiple_statements"),
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
            id="singular_statement",
        ),
        pytest.param(
            ["SUM(column_3)", "column_4"],
            "SELECT column, other_column, SUM(column_3), column_4",
            id="multiple_statements",
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
        pytest.param(["*"], "SELECT *", id="singular_select"),
        pytest.param(["%s"], "SELECT %s", id="select_with_parameter"),
        pytest.param(["'USD'"], "SELECT 'USD'", id="select_constant"),
        pytest.param(
            [1, "2", 3.14, (12, 44)],
            "SELECT 1, 2, 3.14, (12, 44)",
            id="multiple_selects_list_variate_types",
        ),
        pytest.param(["1", "2", "3"], "SELECT 1, 2, 3", id="multiple_selects_list"),
        pytest.param(("1", "2", "3"), "SELECT 1, 2, 3", id="multiple_selects_tuple"),
        pytest.param(
            # Use dict for set-like behaviour because sets are unordered so this test
            # would fail intermittently if using a set
            {"1": None, "2": None, "3": None},
            "SELECT 1, 2, 3",
            id="multiple_selects_set",
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
