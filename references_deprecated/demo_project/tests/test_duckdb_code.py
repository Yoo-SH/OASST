import duckdb
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from sql_metadata import Parser

## https://medium.com/clarityai-engineering/unit-testing-sql-queries-with-duckdb-23743fd22435
## https://www.google.com/search?q=duckdb+test+code+python
## ## https://github.com/duckdb/duckdb/tree/main/tools/pythonpkg/tests


class TestOrderUser:
    def setup(self):
        self.replacements = {
            "my_database.my_schema.my_order_table": "order_table",
            "my_database.my_schema.my_user_table": "user_table",
        }
        with open("s3duckdb/order_user.sql") as f:
            self.query = f.read()

    def test_query(self, order_table: pd.DataFrame, user_table: pd.DataFrame):
        query = self.query
        tables = Parser(self.query).tables
        for table in tables:
            if table in self.replacements:
                query = query.replace(table, self.replacements[table])

        result = duckdb.query(query).to_df()

        assert_frame_equal(
            result,
            pd.DataFrame(
                [{"order_id": 1, "order_value": 9.9, "email": "user_a@domain.fr"}]
            ),
        )

    @pytest.fixture
    def order_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"order_id": 1, "order_value": 9.9, "user_id": "a"},
                {"order_id": 2, "order_value": 8.9, "user_id": "b"},
                {"order_id": 3, "order_value": 15.5, "user_id": "c"},
            ]
        )

    @pytest.fixture
    def user_table(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {"id": "a", "email": "user_a@domain.fr"},
                {"id": "b", "email": "user_b@domain.de"},
            ]
        )