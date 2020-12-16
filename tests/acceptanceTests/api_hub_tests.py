import unittest
from datetime import date

import mock
from data.api_hub import Apihub


class Test_api_hub_Methods(unittest.TestCase):
    def setUp(self):
        self.helper = Apihub()

    def test_can_download_from_tiingo_US(self):
        result = self.helper.download_candle('TSLA', '2020-12-8', '2020-12-9')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['close'], 649.88)
        self.assertEqual(result[0]['date'], '2020-12-08T00:00:00.000Z')
        self.assertEqual(result[1]['close'], 604.48)
        self.assertEqual(result[1]['date'], '2020-12-09T00:00:00.000Z')

    def test_can_download_from_tiingo_CN(self):
        result = self.helper.download_candle('300552', '2020-12-8', '2020-12-9')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['close'], 38.7)
        self.assertEqual(result[0]['date'], '2020-12-08T00:00:00.000Z')
        self.assertEqual(result[1]['close'], 43.17)
        self.assertEqual(result[1]['date'], '2020-12-09T00:00:00.000Z')

    @mock.patch('data.api_hub.Apihub._price_url')
    def test_download_from_tiingo_unsuccess(self, mock_price_url):
        self.helper._price_url.return_value = "{}/{}/prices?&token=123".format(self.helper.root_url, "tsla")

        with self.assertRaises(ValueError) as context:
            self.helper.download_candle('TSLA', '2020-12-8', '2020-12-9')
        self.assertTrue('ERROR: can not download ' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
