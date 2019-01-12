import unittest

import stickmanutils


class TestStringMethods(unittest.TestCase):
    def test_withinx1_co1_entirelyinside_co2(self):
        co1 = stickmanutils.Coords(1, 1, 2, 2)
        co2 = stickmanutils.Coords(1, 1, 10, 10)

        result = stickmanutils.within_x(co1, co2)

        self.assertTrue(result)

    def test_withinx1_co1_entirelyoutside_co2(self):
        co1 = stickmanutils.Coords(100, 100, 101, 101)
        co2 = stickmanutils.Coords(1, 1, 10, 10)

        result = stickmanutils.within_x(co1, co2)

        self.assertFalse(result)