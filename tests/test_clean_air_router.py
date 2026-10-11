"""
Unit Tests for VayuRakshak Clean Air Corridor Routing Engine
Author: Bhomesh Razdan (Lead Architect)
"""

import unittest
from src.services.aqi_engine import AQIEngine
from src.services.clean_air_router import CleanAirRouter

class TestCleanAirRouter(unittest.TestCase):

    def setUp(self):
        self.aqi_engine = AQIEngine()
        self.router = CleanAirRouter(self.aqi_engine)

    def test_clean_route_planning(self):
        # Route from DTU (North Delhi) to Connaught Place (Central Delhi)
        route = self.router.plan_route(28.7499, 77.1170, 28.6315, 77.2167, mode="commuter")
        
        self.assertIn("direct_route", route)
        self.assertIn("clean_air_corridor", route)
        self.assertIn("impact_summary", route)
        
        direct = route["direct_route"]
        clean = route["clean_air_corridor"]
        
        # Clean route average AQI must be lower than direct arterial road
        self.assertLess(clean["average_aqi"], direct["average_aqi"])
        
        # Cumulative PM2.5 inhalation dose should be significantly reduced (>15%)
        self.assertGreater(clean["dose_reduction_pct"], 15.0)
        self.assertLess(clean["cumulative_pm25_dose_ug"], direct["cumulative_pm25_dose_ug"])

if __name__ == "__main__":
    unittest.main()
