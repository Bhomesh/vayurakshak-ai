"""
Unit Tests for VayuRakshak Satellite Stubble Burning Tracker
Author: Bhomesh Razdan (Lead Architect)
"""

import unittest
from src.services.stubble_tracker import StubbleBurningTracker

class TestStubbleTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = StubbleBurningTracker()

    def test_incident_detection(self):
        incidents = self.tracker.get_all_incidents()
        self.assertGreater(len(incidents), 5)
        for inc in incidents:
            self.assertIn(inc.state, ["Punjab", "Haryana"])
            self.assertGreater(inc.frp_mw, 0)
            self.assertGreater(inc.estimated_smoke_plume_km, 10.0)

    def test_regional_threat_assessment(self):
        assessment = self.tracker.get_regional_threat_assessment()
        self.assertIn("stubble_impact_index_sbii", assessment)
        self.assertIn("impact_risk_level", assessment)
        self.assertIn("recommended_municipal_action", assessment)
        self.assertTrue(0 <= assessment["stubble_impact_index_sbii"] <= 100)
        self.assertGreater(assessment["nearest_fire_distance_km"], 0)

if __name__ == "__main__":
    unittest.main()
