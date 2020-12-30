import unittest
from datetime import date

import mock
from data.db_helper import DbHelper


class Test_ACCEPTANCE_db_helper_Methods(unittest.TestCase):
    def setUp(self):
        self.helper = DbHelper()
        self.test_table_name = "TEST"
        self.real_table_name = "US_TSLA"

    def tearDown(self):
        if self.helper.table_exists(self.test_table_name):
            self.helper.drop_table(self.test_table_name)

    def test_insert_tick_data_with_no_date(self):
        if (self.helper.table_exists(self.test_table_name)):
            self.helper.drop_table(self.test_table_name)
        self.helper.create_table(self.test_table_name)
        self.helper.insert_tick_data(self.test_table_name, [])

    def test_get_latest_date_from_empty_table(self):
        if (self.helper.table_exists(self.test_table_name)):
            self.helper.drop_table(self.test_table_name)
        self.helper.create_table(self.test_table_name)

        result = self.helper._latest_date_in_db(self.test_table_name)
        expected_result = date(2081, 1, 1)
        self.assertEqual(result, expected_result)

    def test_insert_and_fetch(self):
        stock_list = [
            ("2010-01-05", 1.0, 4567, 0,       0, 0, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
            ("2010-01-07", 3.0, 6789, 0,       0, 0,  1, date.today(), date.today())
        ]

        if (self.helper.table_exists(self.test_table_name)):
            self.helper.drop_table(self.test_table_name)

        self.helper.create_table(self.test_table_name)
        self.helper.insert_tick_data(self.test_table_name, stock_list)

        _query = "SELECT * FROM stock.{} order by stock_date desc".format(self.test_table_name)
        result = self.helper._fetch_all(_query)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][2], 6789)

    def test_stock_data_for_days(self):
        result = self.helper.stock_data_for_days(self.real_table_name, 3)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(result[0]), 9)  # 9 columns

    def test_stock_data_since_date(self):
        result = self.helper.stock_data_since_date(self.real_table_name, '2020-12-01')
        self.assertGreaterEqual(len(result), 13)

    def test_closest_date(self):
        result = self.helper.closest_date(self.real_table_name, '2020-12-01')
        self.assertEqual(result, date(2020, 12, 1))

    def test_closest_date_sunday(self):
        result = self.helper.closest_date(self.real_table_name, '2020-12-06')
        self.assertEqual(result, date(2020, 12, 7))

    @mock.patch('data.db_helper.DbHelper._read_json')
    def test_insert_stock_data_to_db_correctly(self, mock_read_json):
        self.helper._read_json.return_value = {'date': ["2012-01-04", "2012-01-05", "2012-01-06"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}

        if (self.helper.table_exists(self.test_table_name)):
            self.helper.drop_table(self.test_table_name)
        self.helper.create_table(self.test_table_name)
        result_list = self.helper.insert_stock_data_to_db(self.test_table_name)
        self.assertEqual(len(result_list), 3)

        self.helper._read_json.return_value = {'date': ["2012-01-06", "2012-01-07", "2012-01-08"],
                                               'c': [1, 2, 3],
                                               'v': [10, 20, 30],
                                               '3': [1, 2, 3],
                                               '13': [11, 12, 13],
                                               '34': [31, 32, 33],
                                               'BULL': [-1, 0, 1],
                                               'sp': [1.0, 1.0, 1.0]}
        result_list = self.helper.insert_stock_data_to_db(self.test_table_name)
        self.assertEqual(len(result_list), 2)

        _query = "SELECT * FROM stock.{} order by stock_date desc".format(self.test_table_name)
        result = self.helper._fetch_all(_query)
        self.assertEqual(len(result), 5)
        self.assertEqual(int(result[2][1]), 3)
        self.assertEqual(result[2][6], 1)


if __name__ == '__main__':
    unittest.main()
