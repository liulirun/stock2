import unittest
from datetime import date

import mock
from data.fetch_stock_data_from_api import ApiFetch


class Test_ACCEPTANCE_api_hub_Methods(unittest.TestCase):
    def setUp(self):
        self.helper = ApiFetch()

    def test_can_download_from_tiingo_US(self):
        result = self.helper.fetch_from_api("TSLA", "2020-12-8", "2020-12-9")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["close"], 649.88)
        self.assertEqual(result[0]["date"], "2020-12-08T00:00:00.000Z")
        self.assertEqual(result[1]["close"], 604.48)
        self.assertEqual(result[1]["date"], "2020-12-09T00:00:00.000Z")

    def test_can_download_from_tiingo_CN(self):
        result = self.helper.fetch_from_api("300552", "2020-12-8", "2020-12-9")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["close"], 38.7)
        self.assertEqual(result[0]["date"], "2020-12-08T00:00:00.000Z")
        self.assertEqual(result[1]["close"], 43.17)
        self.assertEqual(result[1]["date"], "2020-12-09T00:00:00.000Z")

    @mock.patch("data.fetch_stock_data_from_api.ApiFetch._price_url")
    def test_download_from_tiingo_unsuccess(self, mock_price_url):
        self.helper._price_url.return_value = "{}/{}/prices?&token=123".format(
            self.helper.root_url, "tsla"
        )

        with self.assertRaises(ValueError) as context:
            self.helper.fetch_from_api("TSLA", "2020-12-8", "2020-12-9")
        self.assertTrue("ERROR: can not download " in str(context.exception))


if __name__ == "__main__":
    unittest.main()
