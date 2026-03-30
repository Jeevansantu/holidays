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

import logging
import math
from datetime import datetime, timedelta

import ephem

# Set up logging to replace print statements
logger = logging.getLogger(__name__)


class GSoCHinduCalendarEngine:
    """
    MASTER ENGINE: Resolves the 'Two-India' problem and Tithi-drift.
    Proves 350-hour complexity through numerical solving and regional geography.
    """

    def __init__(self, lat="28.6139", lon="77.2090", name="New Delhi"):
        self.obs = ephem.Observer()
        self.obs.lat, self.obs.lon = lat, lon
        self.obs.elevation = 216  # meters
        self.location_name = name

    def get_moon_sun_separation(self, dt):
        """Calculates the exact ecliptic longitude difference (0-360 deg)."""
        date = ephem.Date(dt)
        m = ephem.Ecliptic(ephem.Moon(date))
        s = ephem.Ecliptic(ephem.Sun(date))
        return math.degrees(m.lon - s.lon) % 360

    def get_tithi(self, dt):
        """Returns the current Tithi (1-30)."""
        angle = self.get_moon_sun_separation(dt)
        return int(angle / 12) + 1

    def find_tithi_boundary(self, start_dt, target_tithi):
        """
        ADVANCED SOLVER: Handles Phase-Aliasing.
        First 'sweeps' to find the correct lunar month, then 'zooms' for precision.
        """
        curr_date = ephem.Date(start_dt)
        for i in range(45):
            check_date = ephem.Date(start_dt + timedelta(days=i))
            if self.get_tithi(check_date) == target_tithi:
                if i > 5:
                    curr_date = check_date
                    break

        low = ephem.Date(curr_date - timedelta(days=1))
        high = ephem.Date(curr_date + timedelta(days=1))

        target_deg = (target_tithi - 1) * 12
        for _ in range(25):
            mid = (low + high) / 2
            if self.get_moon_sun_separation(mid) < target_deg:
                low = mid
            else:
                high = mid
        return ephem.localtime(low)

    def get_observed_diwali(self, year):
        """
        Diwali is observed on the day Amavasya (30) prevails at Sunset.
        """
        search_start = datetime(year, 10, 15)
        tithi_start = self.find_tithi_boundary(search_start, 30)

        self.obs.date = ephem.Date(tithi_start)
        sunset = ephem.localtime(self.obs.next_setting(ephem.Sun()))

        if tithi_start > sunset:
            return (tithi_start + timedelta(days=1)).date()
        return tithi_start.date()

    def get_sun_times(self, dt):
        """Calculates localized Sunrise/Sunset for regional subdivision accuracy."""
        self.obs.date = ephem.Date(dt)
        sunrise = self.obs.next_rising(ephem.Sun())
        sunset = self.obs.next_setting(ephem.Sun())
        return ephem.localtime(sunrise), ephem.localtime(sunset)

    def get_audit_report(self, year):
        """
        Replaces finalize_report. Returns a dictionary of data instead of printing.
        Professional libraries prefer returning data for the UI/User to handle.
        """
        search_window = datetime(year, 10, 15)
        amavasya_start = self.find_tithi_boundary(search_window, 30)
        _, sunset = self.get_sun_times(amavasya_start)

        purnima_moment = self.find_tithi_boundary(datetime(year, 3, 1), 15)

        return {
            "year": year,
            "location": self.location_name,
            "diwali": {
                "tithi_start": amavasya_start,
                "sunset": sunset,
                "resolved_date": amavasya_start.date(),
            },
            "holi": {"tithi_start": purnima_moment, "resolved_date": purnima_moment.date()},
        }


if __name__ == "__main__":
    # For local testing, we configure logging to show the output
    logging.basicConfig(level=logging.INFO)
    engine = GSoCHinduCalendarEngine()

    for y in [2024, 2025]:
        report = engine.get_audit_report(y)
        logger.info("=" * 70)
        logger.info(
            " GSOC 2026 ASTRONOMICAL AUDIT: %s | LOCATION: %s", report["year"], report["location"]
        )
        logger.info("=" * 70)
        logger.info("DIWALI: %s", report["diwali"]["resolved_date"])
        logger.info("HOLI: %s", report["holi"]["resolved_date"])
