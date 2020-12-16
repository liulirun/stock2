import unittest
from datetime import date

import mock
from data.db_helper import DbHelper


class Test_db_helper_Methods(unittest.TestCase):
    def test_insert_tick_data_with_no_date(self):
        helper = DbHelper()
        table_name = "TEST"

        if (helper.table_exists(table_name)):
            helper.drop_table(table_name)
        helper.create_table(table_name)
        helper.insert_tick_data(table_name, [])
        self.assert_(True)

    def test_get_latest_date_from_empty_table(self):
        helper = DbHelper()
        table_name = "TEST"

        if (helper.table_exists(table_name)):
            helper.drop_table(table_name)
        helper.create_table(table_name)

        result = helper._latest_date_in_db(table_name)
        expected_result = date(2081, 1, 1)
        self.assertEqual(result, expected_result)

    def test_insert_and_fetch(self):
        helper = DbHelper()
        stock_list = [
            ("2010-01-05", 1.0, 4567, 0,       0, 0, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
            ("2010-01-07", 3.0, 6789, 0,       0, 0,  1, date.today(), date.today())
        ]
        table_name = "TEST"

        if (helper.table_exists(table_name)):
            helper.drop_table(table_name)

        helper.create_table(table_name)
        helper.insert_tick_data(table_name, stock_list)

        _query = "SELECT * FROM stock.{} order by stock_date desc".format(table_name)
        result = helper._fetch_all(_query)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][2], 6789)

    @mock.patch('data.db_helper.DbHelper._read_json')
    def test_insert_stock_data_to_db_correctly(self, mock_read_json):
        helper = DbHelper()
        helper._read_json.return_value = {'date': ["2012-01-04", "2012-01-05", "2012-01-06"],
                                          'c': [1, 2, 3],
                                          'v': [10, 20, 30],
                                          '3': [1, 2, 3],
                                          '13': [11, 12, 13],
                                          '34': [31, 32, 33],
                                          'BULL': [-1, 0, 1]}
        table_name = "TEST"
        if (helper.table_exists(table_name)):
            helper.drop_table(table_name)
        helper.create_table(table_name)
        result_list = helper.insert_stock_data_to_db(table_name)
        self.assertEqual(len(result_list), 3)

        helper._read_json.return_value = {'date': ["2012-01-06", "2012-01-07", "2012-01-08"],
                                          'c': [1, 2, 3],
                                          'v': [10, 20, 30],
                                          '3': [1, 2, 3],
                                          '13': [11, 12, 13],
                                          '34': [31, 32, 33],
                                          'BULL': [-1, 0, 1]}
        result_list = helper.insert_stock_data_to_db(table_name)
        self.assertEqual(len(result_list), 2)

        _query = "SELECT * FROM stock.{} order by stock_date desc".format(table_name)
        result = helper._fetch_all(_query)
        self.assertEqual(len(result), 5)
        self.assertEqual(int(result[2][1]), 3)
        self.assertEqual(result[2][6], 1)


if __name__ == '__main__':
    unittest.main()
