import unittest

# import mock
from data.fetch_stock_data_from_api import ApiFetch


class Test_UNIT_api_hub_Method(unittest.TestCase):
    def setUp(self):
        self.helper = ApiFetch()

    def test_happy_path(self):
        tiingo_list = [
            {
                "date": "2019-01-02T00:00:00.000Z",
                "close": 157.92,
                "adjClose": 157.92,
                "adjVolume": 37039737,
                "splitFactor": 1.0,
            },
            {
                "date": "2019-01-03T00:00:00.000Z",
                "close": 142.19,
                "adjClose": 142.19,
                "adjVolume": 91312195,
                "splitFactor": 1.0,
            },
            {
                "date": "2019-01-04T00:00:00.000Z",
                "close": 148.26,
                "adjClose": 148.26,
                "adjVolume": 58607070,
                "splitFactor": 1.0,
            },
            {
                "date": "2019-01-07T00:00:00.000Z",
                "close": 147.93,
                "adjClose": 147.93,
                "adjVolume": 54777764,
                "splitFactor": 5.0,
            },
        ]

        result = self.helper.convert_candle_data(tiingo_list)
        self.assertEqual(len(result), 8)
        self.assertEqual(len(result["date"]), 4)
        self.assertGreater(result["3"][2], 140)
        self.assertEqual(result["BULL"], [-1, -1, -1, -1])
        self.assertEqual(result["sp"], [1.0, 1.0, 1.0, 5.0])

    def test_empty_tiingo_list(self):
        tiingo_list = []
        with self.assertRaises(ValueError) as context:
            self.helper.convert_candle_data(tiingo_list)
        self.assertTrue("tiingo list has error!" in str(context.exception))

    def test_wrong_date_formatin_tiingo_keys(self):
        tiingo_list = [
            {
                "date": "2019-01-01 00:00:00.000",
                "close": 157.92,
                "adjClose": 157.92,
                "adjVolume": 37039737,
            },
            {
                "date": "2019-01-02T00:00:00.000Z",
                "close": 148.26,
                "adjClose": 148.26,
                "adjVolume": 58607070,
            },
        ]

        with self.assertRaises(ValueError) as context:
            self.helper.convert_candle_data(tiingo_list)
        self.assertTrue("tiingo list has error!" in str(context.exception))

    def test_no_date_in_tiingo_keys(self):
        tiingo_list = [
            {
                "date": "2019-01-02T00:00:00.000Z",
                "close": 157.92,
                "adjClose": 157.92,
                "adjVolume": 37039737,
            },
            {"close": 148.26, "adjClose": 148.26, "adjVolume": 58607070},
        ]

        with self.assertRaises(ValueError) as context:
            self.helper.convert_candle_data(tiingo_list)
        self.assertTrue("tiingo list has error!" in str(context.exception))

    def test_no_adjClose_in_tiingo_keys(self):
        tiingo_list = [
            {
                "date": "2019-01-01T00:00:00.000Z",
                "close": 157.92,
                "adjClose": 157.92,
                "adjVolume": 37039737,
            },
            {
                "date": "2019-01-02T00:00:00.000Z",
                "close": 148.26,
                "adjVolume": 58607070,
            },
        ]

        with self.assertRaises(ValueError) as context:
            self.helper.convert_candle_data(tiingo_list)
        self.assertTrue("tiingo list has error!" in str(context.exception))

    def test_no_adjVolume_in_tiingo_keys(self):
        tiingo_list = [
            {
                "date": "2019-01-02T00:00:00.000Z",
                "close": 157.92,
                "adjClose": 157.92,
                "adjVolume": 37039737,
            },
            {"date": "2019-01-02T00:00:00.000Z", "close": 148.26, "adjClose": 148.26},
        ]

        with self.assertRaises(ValueError) as context:
            self.helper.convert_candle_data(tiingo_list)
        self.assertTrue("tiingo list has error!" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
