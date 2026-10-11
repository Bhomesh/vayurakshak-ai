"""
VayuRakshak AI - Core Data Models and Constants
Author: Bhomesh Razdan (Lead Architect)
Event: Bharat Builds Tour - Environmental Hacks (WeMakeDevs x AWS)
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import time

class AQICategory(str, Enum):
    GOOD = "Good"                 # 0-50
    SATISFACTORY = "Satisfactory" # 51-100
    MODERATE = "Moderate"         # 101-200
    POOR = "Poor"                 # 201-300
    VERY_POOR = "Very Poor"       # 301-400
    SEVERE = "Severe"             # 401-500
    HAZARDOUS = "Hazardous"       # 500+

class UserVulnerability(str, Enum):
    GENERAL_PUBLIC = "general_public"
    CHILDREN_STUDENTS = "children_students"
    ASTHMA_RESPIRATORY = "asthma_respiratory"
    ELDERLY = "elderly"
    OUTDOOR_WORKERS = "outdoor_workers"

@dataclass
class AirQualityStation:
    station_id: str
    name: str
    city: str
    state: str
    latitude: float
    longitude: float
    pm25: float
    pm10: float
    no2: float
    so2: float
    co: float
    aqi: int
    category: AQICategory
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['category'] = self.category.value
        return d

@dataclass
class StubbleFireIncident:
    fire_id: str
    latitude: float
    longitude: float
    brightness_kelvin: float
    frp_mw: float  # Fire Radiative Power in MegaWatts
    confidence_score: float # 0.0 - 1.0
    detected_at: str
    district: str
    state: str
    estimated_smoke_plume_km: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RouteCoordinate:
    lat: float
    lon: float
    name: Optional[str] = None

@dataclass
class OptimizedPathSegment:
    from_point: RouteCoordinate
    to_point: RouteCoordinate
    distance_km: float
    estimated_aqi: int
    pm25_exposure_ug_m3: float
    cleanliness_score: float # 0 - 100

@dataclass
class CleanAirRouteResult:
    route_type: str # "Clean Air Corridor" vs "Shortest Direct Path"
    total_distance_km: float
    estimated_duration_mins: float
    average_aqi: int
    cumulative_pm25_dose_ug: float
    dose_reduction_pct: float
    waypoints: List[Dict[str, float]]
    safety_summary: str
    recommended_mask: str

@dataclass
class HealthAdvisory:
    vulnerability_group: UserVulnerability
    location_name: str
    current_aqi: int
    primary_pollutant: str
    recommended_actions: List[str]
    school_advisory: str
    outdoor_activity_guidance: str
    mask_recommendation: str
    generated_by: str = "Amazon Bedrock AI Agent (Strands Framework)"
