import unittest

from data.stock_data_helper import StockDataHelper


class Test_UNIT_stock_data_helper_Methods(unittest.TestCase):
    def setUp(self):
        self.helper = StockDataHelper()

    def test_ma_lists(self):
        price_list = range(1, 21)
        expected_ma3 = [0, 0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0,
                        10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]
        expected_ma13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]
        expected_ma34 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ma_3, ma_13, ma_34 = self.helper.ma_lists(price_list)
        self.assertEqual(len(ma_3), 20)
        self.assertEqual(len(ma_13), 20)
        self.assertEqual(len(ma_34), 20)
        self.assertEqual(ma_3, expected_ma3)
        self.assertEqual(ma_13, expected_ma13)
        self.assertEqual(ma_34, expected_ma34)

    def test_bull_list_PriceList_shorter_than_BULL_INTERVAL(self):
        self.helper.BULL_INTERVAL = 20
        price_list = range(0, 19)
        bull_list_expected = [-1 for i in price_list]

        bull_list = self.helper.bull_list(price_list)

        self.assertEqual(len(bull_list), len(bull_list_expected))
        self.assertEqual(bull_list, bull_list_expected)

    def test_bull_list_order_asc(self):
        self.helper.BULL_INTERVAL = 5
        price_list = range(0, 10)
        b_list1 = [-1 for i in range(0, self.helper.BULL_INTERVAL)]
        b_list2 = [1 for i in range(self.helper.BULL_INTERVAL, 10)]
        bull_list_expected = b_list1 + b_list2

        bull_list = self.helper.bull_list(price_list)

        self.assertEqual(len(bull_list), len(price_list))
        self.assertEqual(bull_list, bull_list_expected)

    def test_bull_list_order_desc(self):
        self.helper.BULL_INTERVAL = 5
        price_list = range(10, 0, -1)
        b_list1 = [-1 for i in range(0, self.helper.BULL_INTERVAL)]
        b_list2 = [0 for i in range(self.helper.BULL_INTERVAL, 10)]
        bull_list_expected = b_list1 + b_list2

        bull_list = self.helper.bull_list(price_list)

        self.assertEqual(len(bull_list), len(price_list))
        self.assertEqual(bull_list, bull_list_expected)


if __name__ == '__main__':
    unittest.main()
