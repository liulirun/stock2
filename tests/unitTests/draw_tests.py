import unittest

from analyze.draw_helper import DrawHelper


class Test_UNIT_draw_helper_Method(unittest.TestCase):
        
    def test_happy_path(self):
        stock_tuple = (("2010-01-01", 160.17, 1, 159.17, 155.77, 157.19, 0),
                       ("2010-01-02", 161.44, 2, 160.61, 156.58, 157.21, 0),
                       )
        draw_helper = DrawHelper("test", stock_tuple)
        self.assertEqual(draw_helper.price_list, [160.17, 161.44])


if __name__ == '__main__':
    unittest.main()
