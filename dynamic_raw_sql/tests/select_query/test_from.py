import pytest

from dynamic_raw_sql import SelectQuery


def test_instantiate_query_with_from_clause() -> None:
    query = SelectQuery(from_table="table")

    assert query.build() == "SELECT  FROM table"


def test_add_from_clause_to_empty_query() -> None:
    query = SelectQuery().from_("table")

    assert query.build() == "SELECT  FROM table"


def test_adding_invalid_from_clause_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        SelectQuery().from_(1)

    with pytest.raises(TypeError):
        SelectQuery().from_(["table1", "table2"])


def test_instantiating_with_invalid_from_clause_raises_typeerror() -> None:
    with pytest.raises(TypeError):
        SelectQuery(from_table=1)

    with pytest.raises(TypeError):
        SelectQuery(from_table=["table1", "table2"])


def test_add_from_clause_to_existing_query() -> None:
    query = SelectQuery(
        select_elements=["column_1", "column_2", "SUM(column_3)"]
    ).from_("table")

    assert query.build() == "SELECT column_1, column_2, SUM(column_3) FROM table"
