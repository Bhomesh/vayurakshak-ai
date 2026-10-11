"""
Unit Tests for VayuRakshak AWS Lambda Serverless Handlers
Author: Bhomesh Razdan (Lead Architect)
"""

import unittest
import json
from src.lambda_handlers import (
    handler_get_stations,
    handler_estimate_hyperlocal,
    handler_get_stubble_fires,
    handler_plan_clean_route,
    handler_get_advisory,
    handler_cedar_authorize,
    eventbridge_cron_worker
)

class TestLambdaHandlers(unittest.TestCase):

    def test_handler_get_stations(self):
        event = {"httpMethod": "GET"}
        res = handler_get_stations(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertGreater(body["count"], 0)
        self.assertIn("stations", body)

    def test_handler_estimate_hyperlocal(self):
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {"lat": "28.7499", "lon": "77.1170"}
        }
        res = handler_estimate_hyperlocal(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertIn("estimated_aqi", body)

    def test_handler_get_stubble_fires(self):
        event = {"httpMethod": "GET"}
        res = handler_get_stubble_fires(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertIn("regional_threat", body)

    def test_handler_plan_clean_route(self):
        event = {
            "httpMethod": "POST",
            "body": json.dumps({
                "start_lat": 28.7499,
                "start_lon": 77.1170,
                "end_lat": 28.6139,
                "end_lon": 77.2090
            })
        }
        res = handler_plan_clean_route(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertIn("clean_air_corridor", body)

    def test_handler_get_advisory(self):
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {
                "group": "children_students",
                "aqi": "410",
                "location": "North Delhi / DTU"
            }
        }
        res = handler_get_advisory(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertIn("school_safety_guidance", body)
        self.assertIn("CRITICAL", body["school_safety_guidance"])

    def test_handler_cedar_authorize(self):
        event = {
            "httpMethod": "POST",
            "body": json.dumps({
                "role": "Citizen",
                "action": "Action::ViewAQI",
                "resource": "Telemetry"
            })
        }
        res = handler_cedar_authorize(event)
        self.assertEqual(res["statusCode"], 200)
        body = json.loads(res["body"])
        self.assertEqual(body["decision"], "ALLOW")

    def test_eventbridge_cron_worker(self):
        res = eventbridge_cron_worker({})
        self.assertEqual(res["status"], "SUCCESS")

if __name__ == "__main__":
    unittest.main()
