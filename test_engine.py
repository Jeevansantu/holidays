import unittest
from datetime import date, datetime
from hindu_engine_v1 import GSoCHinduCalendarEngine

class TestHinduEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GSoCHinduCalendarEngine()

    def test_2024_diwali_parity(self):
        expected = date(2024, 10, 31)
        calc_moment = self.engine.find_tithi_boundary(datetime(2024, 10, 15), 30)
        print(f"\n[TEST] 2024 Diwali: Expected {expected}, Engine got {calc_moment.date()}")
        self.assertEqual(calc_moment.date(), expected)

if __name__ == "__main__":
    unittest.main()
