"""
Unit Tests for VayuRakshak NAQI Calculation & IDW Interpolation Engine
Author: Bhomesh Razdan (Lead Architect)
"""

import unittest
from src.services.aqi_engine import (
    calculate_sub_index,
    calculate_cpcb_aqi,
    get_category_from_aqi,
    AQIEngine,
    BREAKPOINTS_PM25,
    haversine_distance
)
from src.core.models import AQICategory

class TestAQIEngine(unittest.TestCase):

    def test_sub_index_pm25(self):
        # 15 ug/m3 -> Good (halfway between 0 and 30 is 25)
        sub = calculate_sub_index(15.0, BREAKPOINTS_PM25)
        self.assertEqual(sub, 25)

        # 60 ug/m3 -> Top of Satisfactory (100)
        sub = calculate_sub_index(60.0, BREAKPOINTS_PM25)
        self.assertEqual(sub, 100)

        # 250 ug/m3 -> Severe threshold (400)
        sub = calculate_sub_index(250.0, BREAKPOINTS_PM25)
        self.assertEqual(sub, 400)

    def test_cpcb_aggregate_aqi(self):
        # PM2.5 = 250 (sub-index 400), PM10 = 350 (sub-index 300) -> Max should be 400 (Severe)
        aqi, cat, lead = calculate_cpcb_aqi(pm25=250.0, pm10=350.0)
        self.assertEqual(aqi, 400)
        self.assertEqual(cat, AQICategory.VERY_POOR) # 400 is boundary of Very Poor / Severe
        self.assertEqual(lead, "PM2.5")

    def test_haversine_distance(self):
        # DTU Bawana (28.7499, 77.1170) to Connaught Place (28.6315, 77.2167) is ~16-18 km
        dist = haversine_distance(28.7499, 77.1170, 28.6315, 77.2167)
        self.assertTrue(14.0 < dist < 20.0, f"Distance expected ~16-18km, got {dist}")

    def test_idw_hyperlocal_estimation(self):
        engine = AQIEngine()
        # Test DTU Bawana station coordinate
        res = engine.estimate_hyperlocal_aqi(28.7499, 77.1170)
        self.assertIn("estimated_aqi", res)
        self.assertIn("category", res)
        self.assertTrue(res["estimated_aqi"] > 0)
        self.assertEqual(res["confidence"], "Exact Sensor Match")

if __name__ == "__main__":
    unittest.main()
