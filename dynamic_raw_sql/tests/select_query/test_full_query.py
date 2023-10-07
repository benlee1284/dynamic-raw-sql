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
        where_conditions=[
            "1=1",
            "column_1=42",
            "column_2=144 OR column_3=20"
        ],
        group_by_elements=[
            "column_1",
            "column_2",
        ],
    )
    assert (
        query.build()
        == "SELECT column_1, column_2, SUM(column_3), 1 "
        "FROM table WHERE 1=1 AND column_1=42 AND column_2=144 OR column_3=20 "
        "GROUP BY column_1, column_2"
    )
