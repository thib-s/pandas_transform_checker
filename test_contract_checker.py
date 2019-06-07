import unittest
from unittest import TestCase
import pandas as pd

from pandas_transform_checker.decorator_contract_checker import input_df_contract


class Test_contract_checker(TestCase):

    @staticmethod
    def get_dataFrame():
        return pd.DataFrame(pd.np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                            columns=['a', 'b', 'c'],
                            dtype="int",
                            index=pd.DatetimeIndex(
                                freq='D',
                                start=pd.datetime(2019, 5, 20),
                                periods=3))

    @staticmethod
    def _transform_change_index(df:pd.DataFrame):
        df = df.copy()
        return df.resample('3T', label='right').sum()

    @staticmethod
    def _transform_add_column(df:pd.DataFrame, col_name, value):
        df = df.copy()
        df[col_name] = value
        return df

    @staticmethod
    def _transform_remove_column(df:pd.DataFrame, col_name):
        df = df.copy()
        df.drop(col_name, inplace=True, axis=1)
        return df

    @staticmethod
    def _transform_edit_column(df:pd.DataFrame, col_name):
        df = df.copy()
        df[col_name] = 3.1415
        return df

    @staticmethod
    def _transform_change_dtype(df:pd.DataFrame, col_name, new_dtype):
        df:pd.DataFrame = df.copy()
        return df.astype({col_name: new_dtype})

    def test_addition(self):
        df = self.get_dataFrame()
        # self.assertRaises()
        @input_df_contract(df_param="df", contract_params={"col_additions": {"A": "int"}})
        def col_addition_ok(df: pd.DataFrame):
            return self._transform_add_column(df=df, col_name="A", value=1)

        @input_df_contract(df_param="df", contract_params={"col_additions": {"A": "int", "B":"float"}})
        def col_addition_ok2(df: pd.DataFrame):
            return df.pipe(self._transform_add_column, col_name="A", value=1)\
                .pipe(self._transform_add_column, col_name="B", value=1.75)

        @input_df_contract(df_param="df", contract_params={"col_additions": {"A": "int"}})
        def col_addition_wrong_name(df: pd.DataFrame):
            return self._transform_add_column(df=df, col_name="B", value=1)

        @input_df_contract(df_param="df", contract_params={"col_additions": {"A": "int"}})
        def col_addition_wrong_type(df: pd.DataFrame):
            return self._transform_add_column(df, "A", 1.75)

        @input_df_contract(df_param="df", contract_params={"col_additions": {"A": "int"}})
        def col_addition_no_addition(df: pd.DataFrame):
            return df

        @input_df_contract(df_param="df", contract_params={"col_additions": {"a": "int"}})
        def col_addition_already_exist(df: pd.DataFrame):
            return df

        # should not fail
        col_addition_ok(df)
        col_addition_ok2(df)
        # should fail:
        with self.assertRaises(AssertionError, msg="must raise error when no column is created") as cm:
            col_addition_wrong_name(df)
        with self.assertRaises(AssertionError, msg="must raise error when no column is created") as cm:
            col_addition_wrong_name(df)
        with self.assertRaises(AssertionError, msg="must raise error when type don't meet contract") as cm:
            col_addition_wrong_type(df)
        with self.assertRaises(AssertionError, msg="must raise error when specified column is not created") as cm:
            col_addition_no_addition(df)
        with self.assertRaises(AssertionError, msg="must raise error when column already exist") as cm:
            col_addition_already_exist(df)

    def test_deletion(self):

        df = self.get_dataFrame()

        @input_df_contract(df_param="df", contract_params={"col_deletions": {"a"}})
        def col_delete_ok(df: pd.DataFrame):
            return self._transform_remove_column(df, "a")

        @input_df_contract(df_param="df", contract_params={"col_deletions": {"a", "b"}})
        def col_delete_ok2(df: pd.DataFrame):
            return df.pipe(self._transform_remove_column, col_name="a")\
                .pipe(self._transform_remove_column, col_name="b")
        
        @input_df_contract(df_param="df", contract_params={"col_deletions": {"a"}})
        def col_delete_no_deletion(df: pd.DataFrame):
            return df

        @input_df_contract(df_param="df", contract_params={"col_deletions": {"X"}})
        def col_delete_already_deleted(df: pd.DataFrame):
            return df

        # should not fail
        col_delete_ok(df)
        col_delete_ok2(df)
        # should fail
        with self.assertRaises(AssertionError, msg="must raise error when no column is deleted") as cm:
            col_delete_no_deletion(df)
        with self.assertRaises(AssertionError, msg="must raise error when column already deleted") as cm:
            col_delete_already_deleted(df)

    def test_edition(self):
        df = self.get_dataFrame()

        @input_df_contract(df_param="df", contract_params={"col_editions": {"a"}})
        def col_edit_ok(df: pd.DataFrame):
            return self._transform_edit_column(df, "a")

        @input_df_contract(df_param="df", contract_params={"col_editions": {"a", "b"}})
        def col_edit_ok2(df: pd.DataFrame):
            return df.pipe(self._transform_edit_column, col_name="a") \
                .pipe(self._transform_edit_column, col_name="b")

        @input_df_contract(df_param="df", contract_params={"col_editions": {"a"}})
        def col_delete_edit_wrong_col(df: pd.DataFrame):
            return self._transform_edit_column(df, "b")

        # should not fail
        col_edit_ok(df)
        col_edit_ok2(df)
        # should fail
        with self.assertRaises(AssertionError, msg="must raise error when the wrong column is edited") as cm:
            col_delete_edit_wrong_col(df)

    def test_index_edition(self):
        df = self.get_dataFrame()

        @input_df_contract(df_param="df", contract_params={"allow_index_edition": True})
        def index_edit_ok(df: pd.DataFrame):
            return self._transform_change_index(df)

        @input_df_contract(df_param="df", contract_params={"allow_index_edition": False})
        def index_edit_ko(df: pd.DataFrame):
            return self._transform_change_index(df)

        # should not fail
        index_edit_ok(df)
        # should fail
        with self.assertRaises(AssertionError, msg="must raise error when the index is edited while allow_index_edition is set to False") as cm:
            index_edit_ko(df)

    def test_all(self):
        df = self.get_dataFrame()

        @input_df_contract(df_param="df",
                           contract_params={
                               "col_additions": {"added_1": "float"},
                               "col_deletions": {"b"},
                               "col_editions": {"a"},
                               "allow_index_edition": False
                           })
        def modification_ok(df: pd.DataFrame):
            return df.pipe(
                self._transform_edit_column, col_name="a"
            ).pipe(
                self._transform_add_column, col_name="added_1", value=1.75
            ).pipe(
                self._transform_remove_column, col_name="b"
            )

        @input_df_contract(df_param="df",
                           contract_params={
                               "col_additions": {"added_1": "float"},
                               "col_deletions": {"b"},
                               "col_editions": {"b"},# change is here
                               "allow_index_edition": False
                           })
        def modification_ko(df: pd.DataFrame):
            return df.pipe(
                self._transform_edit_column, col_name="a"
            ).pipe(
                self._transform_add_column, col_name="added_1", value=1.75
            ).pipe(
                self._transform_remove_column, col_name="b"
            )

        @input_df_contract(df_param="df",
                           contract_params={
                               "col_additions": {"added_1": "float"},
                               "col_deletions": {"added_1"},
                               "col_editions": {"a"},
                               "allow_index_edition": False
                           })
        def modification_ko2(df: pd.DataFrame):
            return df.pipe(
                self._transform_edit_column, col_name="a"
            ).pipe(
                self._transform_add_column, col_name="added_1", value=1.75
            ).pipe(
                self._transform_remove_column, col_name="b"
            )


if __name__ == '__main__':
    unittest.main()
