"""
VayuRakshak AI - AWS Lambda Handlers & Serverless Integration
Supports AWS API Gateway proxy events, AWS EventBridge periodic triggers, and SNS publish.
Author: Bhomesh Razdan (Lead Architect)
"""

import json
from typing import Dict, Any
from .services.aqi_engine import AQIEngine
from .services.stubble_tracker import StubbleBurningTracker
from .services.clean_air_router import CleanAirRouter
from .services.advisory_agent import AdvisoryAgent
from .services.cedar_auth import CedarPolicyEngine
from .core.models import UserVulnerability

# Singleton service instances in Lambda warm memory
aqi_engine = AQIEngine()
stubble_tracker = StubbleBurningTracker()
clean_router = CleanAirRouter(aqi_engine)
advisory_agent = AdvisoryAgent()
cedar_engine = CedarPolicyEngine()

def build_response(status_code: int, body: Any) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Principal-Role"
        },
        "body": json.dumps(body)
    }

def handler_get_stations(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: returns all CPCB stations and real-time sensor measurements."""
    stations = [s.to_dict() for s in aqi_engine.get_all_stations()]
    return build_response(200, {
        "count": len(stations),
        "source": "Central Pollution Control Board (CPCB) / IoT Station Network",
        "stations": stations
    })

def handler_estimate_hyperlocal(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: Inverse Distance Weighting interpolation for arbitrary coordinate."""
    params = event.get("queryStringParameters") or {}
    try:
        lat = float(params.get("lat", 28.7499)) # default DTU
        lon = float(params.get("lon", 77.1170))
    except ValueError:
        return build_response(400, {"error": "Invalid lat/lon parameters"})
        
    result = aqi_engine.estimate_hyperlocal_aqi(lat, lon)
    return build_response(200, result)

def handler_get_stubble_fires(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: returns active satellite thermal anomalies and regional transport risk."""
    incidents = [i.to_dict() for i in stubble_tracker.get_all_incidents()]
    risk = stubble_tracker.get_regional_threat_assessment()
    return build_response(200, {
        "satellite_source": "NASA FIRMS / ISRO Sentinel-3 Thermal Radiance",
        "incidents": incidents,
        "regional_threat": risk
    })

def handler_plan_clean_route(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: plans clean air corridor between coordinates."""
    # Handle body parsing from POST or query params from GET
    params = {}
    if event.get("httpMethod") == "POST" and event.get("body"):
        try:
            params = json.loads(event["body"])
        except Exception:
            pass
    elif event.get("queryStringParameters"):
        params = event["queryStringParameters"]

    try:
        start_lat = float(params.get("start_lat", 28.7499)) # DTU
        start_lon = float(params.get("start_lon", 77.1170))
        end_lat = float(params.get("end_lat", 28.6139))     # Connaught Place
        end_lon = float(params.get("end_lon", 77.2090))
        mode = params.get("mode", "commuter")
    except ValueError:
        return build_response(400, {"error": "Invalid start or end coordinates"})

    route = clean_router.plan_route(start_lat, start_lon, end_lat, end_lon, mode)
    return build_response(200, route)

def handler_get_advisory(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: generates Bedrock/Strands contextual advisory."""
    params = event.get("queryStringParameters") or {}
    group_str = params.get("group", "general_public")
    try:
        vuln = UserVulnerability(group_str)
    except ValueError:
        vuln = UserVulnerability.GENERAL_PUBLIC

    try:
        aqi = int(params.get("aqi", 380))
    except ValueError:
        aqi = 380

    loc = params.get("location", "Delhi NCR")
    advisory = advisory_agent.generate_advisory(loc, aqi, "Severe", vuln)
    
    return build_response(200, {
        "vulnerability_group": advisory.vulnerability_group.value,
        "location": advisory.location_name,
        "current_aqi": advisory.current_aqi,
        "primary_pollutant": advisory.primary_pollutant,
        "recommended_actions": advisory.recommended_actions,
        "school_safety_guidance": advisory.school_advisory,
        "outdoor_guidance": advisory.outdoor_activity_guidance,
        "recommended_ppe": advisory.mask_recommendation,
        "ai_engine": advisory.generated_by
    })

def handler_cedar_authorize(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda handler: evaluates AWS Cedar authorization policy."""
    try:
        body = json.loads(event.get("body", "{}"))
        role = body.get("role", "Citizen")
        action = body.get("action", "Action::ViewAQI")
        resource = body.get("resource", "Telemetry")
    except Exception:
        return build_response(400, {"error": "Invalid JSON body"})

    allowed, reason = cedar_engine.is_authorized(role, action, resource)
    return build_response(200, {
        "principal_role": role,
        "action": action,
        "resource": resource,
        "decision": "ALLOW" if allowed else "DENY",
        "evaluation_reason": reason,
        "policy_engine": "AWS Cedar v3.1 Policy Store"
    })

def eventbridge_cron_worker(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Invoked every 15 mins by Amazon EventBridge to ingest satellite feeds."""
    assessment = stubble_tracker.get_regional_threat_assessment()
    print(f"[EventBridge Cron] Ingested satellite feed. SBII Impact: {assessment['stubble_impact_index_sbii']}")
    return {"status": "SUCCESS", "sbii": assessment["stubble_impact_index_sbii"]}
