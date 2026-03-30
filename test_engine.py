#  holidays
#  --------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: Vacanza Team and individual contributors (see CONTRIBUTORS file)
#           dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/vacanza/holidays
#  License: MIT (see LICENSE file)

import unittest
from datetime import date

from hindu_engine_v1 import GSoCHinduCalendarEngine


class TestHinduEngine(unittest.TestCase):
    def setUp(self):
        self.engine = GSoCHinduCalendarEngine()

    def test_diwali_validation(self):
        # Official library dates we must match
        expected = {
            2024: date(2024, 10, 31),
            2025: date(2025, 10, 21),  # The logic now handles the Oct 21 shift!
        }

        for year, expected_date in expected.items():
            calc_date = self.engine.get_observed_diwali(year)
            # Use the 'msg' parameter to show details ONLY if the test fails
            self.assertEqual(
                calc_date,
                expected_date,
                msg=f"Year {year}: Expected {expected_date}, but engine calculated {calc_date}",
            )


if __name__ == "__main__":
    unittest.main()
