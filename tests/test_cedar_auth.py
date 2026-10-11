"""
Unit Tests for VayuRakshak AWS Cedar Authorization Policies
Author: Bhomesh Razdan (Lead Architect)
"""

import unittest
from src.services.cedar_auth import CedarPolicyEngine

class TestCedarAuth(unittest.TestCase):

    def setUp(self):
        self.engine = CedarPolicyEngine()

    def test_citizen_permissions(self):
        # Citizen is permitted to view AQI
        allowed, reason = self.engine.is_authorized("Citizen", "Action::ViewAQI", "Telemetry")
        self.assertTrue(allowed)
        self.assertIn("permit_citizen_read", reason)

        # Citizen is DENIED from declaring GRAP emergency
        allowed, reason = self.engine.is_authorized("Citizen", "Action::DeclareGRAPEmergency", "MunicipalAction")
        self.assertFalse(allowed)
        self.assertIn("DENY", reason)

    def test_school_principal_permissions(self):
        # School Principal is permitted to broadcast school advisory
        allowed, reason = self.engine.is_authorized("SchoolPrincipal", "Action::BroadcastSchoolAdvisory", "SchoolSafetyProtocol")
        self.assertTrue(allowed)

        # School Principal is DENIED from halting industrial construction
        allowed, reason = self.engine.is_authorized("SchoolPrincipal", "Action::HaltConstruction", "MunicipalAction")
        self.assertFalse(allowed)

    def test_municipal_officer_permissions(self):
        # Municipal officer permitted to enforce GRAP emergency
        allowed, reason = self.engine.is_authorized("MunicipalOfficer", "Action::DeclareGRAPEmergency", "MunicipalAction")
        self.assertTrue(allowed)
        self.assertIn("permit_municipal_enforcement", reason)

if __name__ == "__main__":
    unittest.main()
