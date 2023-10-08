from dynamic_raw_sql import SelectQuery, UnionedQuery


def test_instantiating_unioned_query_with_select_queries_produces_valid_query() -> None:
    query = UnionedQuery(
        queries=[
            SelectQuery(
                from_table="table",
                select_elements=["*"]
            ),
            SelectQuery(
                from_table="table",
                select_elements=["*"]
            ),
        ]
    )
    assert query.build() == "(SELECT * FROM table) UNION (SELECT * FROM table)"
