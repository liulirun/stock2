# import unittest
import unittest
from datetime import date

import mock
from analyze.algo_regression import Algo_Regression


class Test_UNIT_algo_regression_Method(unittest.TestCase):
    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_map_options_to_methods_happy_path(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 0,       0, 0, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
            ("2010-01-07", 3.0, 6789, 0,       0, 0,  1, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma1_greaterthan_ma2_20", "ma1_greaterthan_ma3_20"],
                                          buy_options_or=["ma2_greaterthan_ma3_20", "ma2_greaterthan_ma4_20"],
                                          sell_options_and=["ma1_lessthan_ma2_20", "ma1_lessthan_ma3_20"],
                                          sell_options_or=["ma2_lessthan_ma3_20", "ma2_lessthan_ma4_20"],
                                          start_date=date(2020, 12, 24))
        self.assertEqual(algo_regression.prices, [1.0, 2.0, 3.0])
        self.assertEqual(algo_regression.zeros, [0, 0, 0])

        algo_regression.map_options_to_methods()

        self.assertEqual(algo_regression.stock_name, 'test')
        self.assertEqual(len(algo_regression.buy_methods_and), 2)
        self.assertEqual(algo_regression.buy_methods_and, [['self.ma1', 'self.greaterthan', 'self.ma2', 20], [
                         'self.ma1', 'self.greaterthan', 'self.ma3', 20]])
        self.assertEqual(len(algo_regression.buy_methods_or), 2)
        self.assertEqual(algo_regression.buy_methods_or, [['self.ma2', 'self.greaterthan', 'self.ma3', 20], [
                         'self.ma2', 'self.greaterthan', 'self.ma4', 20]])
        self.assertEqual(len(algo_regression.sell_methods_and), 2)
        self.assertEqual(algo_regression.sell_methods_and, [['self.ma1', 'self.lessthan', 'self.ma2', 20], [
                         'self.ma1', 'self.lessthan', 'self.ma3', 20]])
        self.assertEqual(len(algo_regression.sell_methods_or), 2)
        self.assertEqual(algo_regression.sell_methods_or, [['self.ma2', 'self.lessthan', 'self.ma3', 20], [
                         'self.ma2', 'self.lessthan', 'self.ma4', 20]])

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_map_options_to_methods_none_given(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 0,       0, 0, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
            ("2010-01-07", 3.0, 6789, 0,       0, 0,  1, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=[],
                                          buy_options_or=[],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()

        self.assertEqual(algo_regression.stock_name, 'test')
        self.assertEqual(algo_regression.buy_methods_and, [])
        self.assertEqual(algo_regression.buy_methods_or, [])
        self.assertEqual(algo_regression.sell_methods_and, [])
        self.assertEqual(algo_regression.sell_methods_or, [])

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methods_and_method_sor_both_null(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 0,       0, 0, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
            ("2010-01-07", 3.0, 6789, 0,       0, 0,  1, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=[],
                                          buy_options_or=[],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)

        self.assertFalse(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methodsand_False_methodsor_null(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma3_greaterthan_ma13_20", "ma13_greaterthan_ma34_20"],
                                          buy_options_or=[],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)

        self.assertFalse(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methodsand_False_methodsor_False(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma3_greaterthan_ma13_20", "ma13_greaterthan_ma34_20"],
                                          buy_options_or=["ma13_lessthan_ma34_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)

        self.assertFalse(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methodsand_False_methodsor_True(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma3_greaterthan_ma13_20", "ma13_greaterthan_ma34_20"],
                                          buy_options_or=["ma13_greaterthan_ma34_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)

        self.assertFalse(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_True_if_methodsand_True_methodsor_null(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma3_lessthan_ma13_20", "ma13_greaterthan_ma34_20"],
                                          buy_options_or=[],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)
        self.assertTrue(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_True_if_methodsand_null_methodsor_True(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=[],
                                          buy_options_or=["ma3_lessthan_ma13_20", "ma13_greaterthan_ma34_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)
        self.assertTrue(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_True_if_methodsand_True_methodsor_True(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma13_greaterthan_ma34_20"],
                                          buy_options_or=["ma13_greaterthan_ma3_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)
        self.assertTrue(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methodsand_True_methodsor_False(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=["ma13_greaterthan_ma34_20"],
                                          buy_options_or=["ma13_lessthan_ma3_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)
        self.assertFalse(result)

    @mock.patch('data.db_helper.DbHelper.stock_data_since_date')
    def test_should_func_return_False_if_methodsand_null_methodsor_False(self, mock_stock_data_since_date):
        mock_stock_data_since_date.return_value = (
            ("2010-01-05", 1.0, 4567, 1,       2, 1, -1, date.today(), date.today()),
            ("2010-01-06", 2.0, 5678, 24.2695, 0, 0,  0, date.today(), date.today()),
        )
        algo_regression = Algo_Regression('test',
                                          buy_options_and=[],
                                          buy_options_or=["ma13_lessthan_ma3_20"],
                                          sell_options_and=[],
                                          sell_options_or=[],
                                          start_date=date(2020, 12, 24))

        algo_regression.map_options_to_methods()
        result = algo_regression._should(0, algo_regression.buy_methods_and, algo_regression.buy_methods_or)
        self.assertFalse(result)

    # # TODO: do not use this in unit test
    # def test_real_data(self):
    #     algo_regression = Algo_Regression('US_TSLA',
    #                                       buy_options_and=["ma3_greaterthan_ma13", "ma13_greaterthan_ma34"],
    #                                       buy_options_or=[],
    #                                       sell_options_and=["ma3_lessthan_ma13", "ma13_lessthan_ma34"],
    #                                       sell_options_or=[],
    #                                       start_date=date(2020, 12, 1))
    #     algo_regression.run()
    #     print("x")


if __name__ == '__main__':
    unittest.main()
