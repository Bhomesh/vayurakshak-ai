"""
VayuRakshak AI - Stubble Burning Satellite Tracker & Plume Dispersion Engine
Sensor Simulation: NASA FIRMS (VIIRS/MODIS) Thermal Ingestion & Smoke Plume Modeling
Author: Bhomesh Razdan (Lead Architect)
"""

from typing import List, Dict, Any
import time
from ..core.models import StubbleFireIncident
from .aqi_engine import haversine_distance

class StubbleBurningTracker:
    """Tracks farm fire clusters and estimates transport towards Delhi NCR."""
    
    def __init__(self):
        self._incidents: List[StubbleFireIncident] = []
        self._load_active_fire_clusters()

    def _load_active_fire_clusters(self):
        # Simulated live satellite clusters detected in Punjab/Haryana farm belts
        clusters = [
            ("FIRE-PB-081", 30.2450, 75.8420, 342.5, 48.2, 0.96, "Sangrur", "Punjab"),
            ("FIRE-PB-082", 30.9010, 75.8573, 338.0, 39.5, 0.92, "Ludhiana", "Punjab"),
            ("FIRE-PB-083", 30.2110, 74.9455, 351.2, 54.1, 0.98, "Bathinda", "Punjab"),
            ("FIRE-PB-084", 31.3260, 75.5762, 329.8, 28.4, 0.88, "Jalandhar", "Punjab"),
            ("FIRE-PB-085", 30.3400, 76.3800, 335.1, 35.8, 0.91, "Patiala", "Punjab"),
            ("FIRE-HR-091", 29.6857, 76.9905, 345.0, 42.6, 0.95, "Karnal", "Haryana"),
            ("FIRE-HR-092", 29.8015, 76.3999, 331.4, 31.0, 0.89, "Kaithal", "Haryana"),
            ("FIRE-HR-093", 29.9695, 76.8783, 326.5, 24.3, 0.85, "Kurukshetra", "Haryana"),
        ]
        
        for fid, lat, lon, bright, frp, conf, dist, state in clusters:
            # Plume radius in km scales with Fire Radiative Power (FRP)
            plume_radius = round(frp * 0.75 + 10.0, 1)
            inc = StubbleFireIncident(
                fire_id=fid,
                latitude=lat,
                longitude=lon,
                brightness_kelvin=bright,
                frp_mw=frp,
                confidence_score=conf,
                detected_at="2026-10-11T09:30:00Z",
                district=dist,
                state=state,
                estimated_smoke_plume_km=plume_radius
            )
            self._incidents.append(inc)

    def get_all_incidents(self) -> List[StubbleFireIncident]:
        return self._incidents

    def get_regional_threat_assessment(self, target_lat: float = 28.6139, target_lon: float = 77.2090) -> Dict[str, Any]:
        """
        Assesses stubble burning transport risk to target location (e.g. Delhi NCR)
        using typical North-Westerly winter wind vectors (speed ~14 km/h, direction ~315 deg).
        """
        total_frp = sum(inc.frp_mw for inc in self._incidents)
        avg_confidence = sum(inc.confidence_score for inc in self._incidents) / len(self._incidents) if self._incidents else 0
        
        # Calculate minimum distance to active fire
        distances = [haversine_distance(target_lat, target_lon, inc.latitude, inc.longitude) for inc in self._incidents]
        min_dist = min(distances) if distances else 0.0
        
        # Plume arrival estimate assuming North-Westerly wind (14 km/h)
        wind_speed_kmh = 14.5
        hours_to_reach = round(min_dist / wind_speed_kmh, 1) if min_dist > 0 else 0
        
        # Stubble Burning Impact Index (SBII) 0 - 100
        # High FRP + close proximity + strong alignment = high SBII
        sbii_score = min(100, int(round((total_frp / 300.0) * 60 + max(0, (250 - min_dist) / 250.0) * 40)))
        
        risk_level = "Severe" if sbii_score > 75 else "Moderate" if sbii_score > 40 else "Low"

        return {
            "target_location": "Delhi NCR / DTU Region",
            "active_fire_count": len(self._incidents),
            "cumulative_radiative_power_mw": round(total_frp, 1),
            "average_confidence_pct": round(avg_confidence * 100, 1),
            "nearest_fire_distance_km": round(min_dist, 1),
            "estimated_smoke_arrival_hours": hours_to_reach,
            "wind_condition": "North-Westerly (315°), 14.5 km/h",
            "stubble_impact_index_sbii": sbii_score,
            "impact_risk_level": risk_level,
            "recommended_municipal_action": (
                "Trigger GRAP Stage-IV emergency dust mitigation, ban non-essential construction, "
                "deploy anti-smog water guns, and issue school remote-learning advisory."
                if sbii_score > 70 else "Maintain GRAP Stage-II surveillance."
            )
        }
