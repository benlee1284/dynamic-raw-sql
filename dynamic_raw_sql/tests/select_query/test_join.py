import pytest

from dynamic_raw_sql import SelectQuery


def test_instantiate_query_with_join_clause() -> None:
    query = SelectQuery(joins=[
        "INNER JOIN table2 ON 1=1",
        "LEFT OUTER JOIN table3 ON column_1=column_2",
    ])

    assert (
        query.build() == "SELECT  INNER JOIN table2 ON 1=1 "
        "LEFT OUTER JOIN table3 ON column_1=column_2"
    )
