from dynamic_raw_sql import SelectQuery


def test_full_query() -> None:
    query = SelectQuery(
        from_table="table",
        select_elements=[
            "column_1",
            "column_2",
            "SUM(column_3)",
            "1",
        ],
        joins=[
            "INNER JOIN table2 ON 1=1",
            "LEFT OUTER JOIN table3 ON column_1=column_2",
        ],
        where_conditions=["1=1", "column_1=42", "column_2=144 OR column_3=20"],
        group_by_elements=[
            "column_1",
            "column_2",
        ],
        having_conditions=["1=1", "column_1=42", "column_2=144 OR column_3=20"],
        order_by_elements=[
            "column_1",
            "column_2",
        ],
    )
    assert (
        query.build() == "SELECT column_1, column_2, SUM(column_3), 1 "
        "FROM table "
        "INNER JOIN table2 ON 1=1 "
        "LEFT OUTER JOIN table3 ON column_1=column_2 "
        "WHERE 1=1 AND column_1=42 AND column_2=144 OR column_3=20 "
        "GROUP BY column_1, column_2 "
        "HAVING 1=1 AND column_1=42 AND column_2=144 OR column_3=20 "
        "ORDER BY column_1, column_2"
    )
