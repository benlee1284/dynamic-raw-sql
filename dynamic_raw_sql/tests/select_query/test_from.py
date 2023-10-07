from dynamic_raw_sql import SelectQuery


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
