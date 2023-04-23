import unittest
from datetime import date

import mock

from data.db_helper import DbHelper


class Test_UNIT_db_helper_Method(unittest.TestCase):
    def setUp(self):
        self.helper = DbHelper()

    @mock.patch('data.db_helper.DbHelper._fetch_all')
    def test_current_stock_cn_name_happy_path(self, mock_fetch_all):
        mock_fetch_all.return_value = (('测试1', ''), ('测试2', ''))
        result = self.helper.current_stock_cn_name("mock_tets")
        self.assertEqual(result, '测试1')

    @mock.patch('data.db_helper.DbHelper._fetch_all')
    def test_current_stock_cn_name_null_value(self, mock_fetch_all):
        mock_fetch_all.return_value = ()
        result = self.helper.current_stock_cn_name("mock_tets")
        self.assertEqual(result, '')

    @mock.patch('data.db_helper.DbHelper._fetch_all')
    def test_latest_date_in_db_happy_path(self, mock_fetch):
        mock_fetch.return_value = ((date(2020, 1, 1),),)
        result = self.helper._latest_date_in_db("mock_tets")
        self.assertTrue(isinstance(result, date))
        self.assertEqual(result, date(2020, 1, 1))

    @mock.patch('data.db_helper.DbHelper._fetch_all')
    def test_latest_date_in_db_empty(self, mock_fetch):
        mock_fetch.return_value = ()
        result = self.helper._latest_date_in_db("mock_tets")
        self.assertEqual(result, date(2081, 1, 1))

    @mock.patch('data.db_helper.DbHelper._read_json')
    def test_insert_stock_data_to_db_empty(self, mock_read_json):
        mock_read_json.return_value = {}
        result = self.helper.insert_stock_data_to_db("mock_tets")
        self.assertEqual(len(result), 0)

    @mock.patch('data.db_helper.DbHelper.table_exists')
    @mock.patch('data.db_helper.DbHelper.create_table')
    def test_create_DB_if_not_exists(self, mock_table_exists, mock_create_table):
        self.helper.table_exists.return_value = False
        self.helper.create_table.return_value = None
        self.helper.create_DB_if_not_exists("mock_tests")
        self.assertEqual(self.helper.create_table.called, True)
        self.assertEqual(self.helper.create_table.call_count, 1)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    @mock.patch('data.db_helper.DbHelper.truncate_table')
    def test_insert_stock_data_to_db_happy_path(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data, mock_truncate_table):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 2.0]}
        self.helper._latest_date_in_db.return_value = date(2012, 1, 1)

        result_list = self.helper.insert_stock_data_to_db("mock_tets")

        self.assertEqual(self.helper.insert_tick_data.called, True)
        self.assertEqual(self.helper.insert_tick_data.call_count, 1)
        self.assertEqual(self.helper.truncate_table.called, True)
        self.assertEqual(self.helper.truncate_table.call_count, 1)
        self.assertEqual(len(result_list), 2)
        self.assertEqual(result_list[0][0], "2012-01-02")
        self.assertEqual(result_list[1][0], "2012-01-03")

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    @mock.patch('data.db_helper.DbHelper.truncate_table')
    def test_insert_stock_data_to_db_split_list_none_called(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data, mock_truncate_table):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [5.0, 1.0, 1.0]}
        self.helper._latest_date_in_db.return_value = date(2012, 1, 1)

        result_list = self.helper.insert_stock_data_to_db("mock_tets")

        self.assertEqual(self.helper.insert_tick_data.called, True)
        self.assertEqual(self.helper.insert_tick_data.call_count, 1)
        self.assertEqual(self.helper.truncate_table.called, False)
        self.assertEqual(len(result_list), 2)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    @mock.patch('data.db_helper.DbHelper.truncate_table')
    def test_insert_stock_data_to_db_split_list_called_only_once(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data, mock_truncate_table):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 0.2, 0.3]}
        self.helper._latest_date_in_db.return_value = date(2012, 1, 1)

        result_list = self.helper.insert_stock_data_to_db("mock_tets")

        self.assertEqual(self.helper.truncate_table.called, True)
        self.assertEqual(self.helper.truncate_table.call_count, 1)
        self.assertEqual(len(result_list), 2)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    def test_insert_tick_data_not_being_called(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}
        self.helper._latest_date_in_db.return_value = date(2012, 1, 3)

        result_list = self.helper.insert_stock_data_to_db("mock_tets")

        self.assertEqual(self.helper.insert_tick_data.called, False)
        self.assertEqual(len(result_list), 0)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    def test_insert_stock_data_to_db_no_data_in_DB(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}
        self.helper._latest_date_in_db.return_value = date(2081, 1, 1)

        result_list = self.helper.insert_stock_data_to_db("mock_tets")

        self.assertEqual(self.helper.insert_tick_data.called, True)
        self.assertEqual(len(result_list), 3)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    def test_something_wrong_with_Database_exception(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}
        self.helper._latest_date_in_db.return_value = date(2012, 1, 9)

        with self.assertRaises(ValueError) as context:
            self.helper.insert_stock_data_to_db("mock_tets")
        self.assertTrue('something wrong with Database' in str(context.exception))
        self.assertEqual(self.helper.insert_tick_data.called, False)

    @mock.patch('data.db_helper.DbHelper._read_json')
    @mock.patch('data.db_helper.DbHelper._latest_date_in_db')
    @mock.patch('data.db_helper.DbHelper.insert_tick_data')
    def test_DB_will_have_gap_exception(self, mock_read_json, mock_db_latest_date, mock_insert_tick_data):
        self.helper._read_json.return_value = {'date': ["2012-01-01", "2012-01-02", "2012-01-03"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}
        self.helper._latest_date_in_db.return_value = date(2011, 12, 31)

        with self.assertRaises(ValueError) as context:
            self.helper.insert_stock_data_to_db("mock_tets")
        self.assertTrue('data in DB will have gap' in str(context.exception))
        self.assertEqual(self.helper.insert_tick_data.called, False)


if __name__ == '__main__':
    unittest.main()
