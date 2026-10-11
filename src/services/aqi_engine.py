"""
VayuRakshak AI - National Air Quality Index (NAQI) & CPCB Sensor Engine
Standard: CPCB India Breakpoint Algorithms & Inverse Distance Weighting (IDW)
Author: Bhomesh Razdan (Lead Architect)
"""

import math
from typing import List, Dict, Tuple, Optional
from ..core.models import AirQualityStation, AQICategory

# CPCB Sub-Index Breakpoint tables: (C_low, C_high, I_low, I_high)
BREAKPOINTS_PM25 = [
    (0, 30, 0, 50),
    (31, 60, 51, 100),
    (61, 90, 101, 200),
    (91, 120, 201, 300),
    (121, 250, 301, 400),
    (251, 500, 401, 500)
]

BREAKPOINTS_PM10 = [
    (0, 50, 0, 50),
    (51, 100, 51, 100),
    (101, 250, 101, 200),
    (251, 350, 201, 300),
    (351, 430, 301, 400),
    (431, 600, 401, 500)
]

BREAKPOINTS_NO2 = [
    (0, 40, 0, 50),
    (41, 80, 51, 100),
    (81, 180, 101, 200),
    (181, 280, 201, 300),
    (281, 400, 301, 400),
    (401, 600, 401, 500)
]

def calculate_sub_index(conc: float, breakpoints: List[Tuple[float, float, float, float]]) -> int:
    """Calculates linear sub-index according to CPCB formula."""
    if conc <= 0:
        return 0
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= conc <= c_high:
            sub = ((i_high - i_low) / (c_high - c_low)) * (conc - c_low) + i_low
            return int(round(sub))
    # Above max breakpoint
    last_c_low, last_c_high, last_i_low, last_i_high = breakpoints[-1]
    if conc > last_c_high:
        extra = conc - last_c_high
        return min(999, int(round(last_i_high + extra)))
    return 0

def get_category_from_aqi(aqi: int) -> AQICategory:
    if aqi <= 50:
        return AQICategory.GOOD
    elif aqi <= 100:
        return AQICategory.SATISFACTORY
    elif aqi <= 200:
        return AQICategory.MODERATE
    elif aqi <= 300:
        return AQICategory.POOR
    elif aqi <= 400:
        return AQICategory.VERY_POOR
    elif aqi <= 500:
        return AQICategory.SEVERE
    else:
        return AQICategory.HAZARDOUS

def calculate_cpcb_aqi(pm25: float, pm10: float, no2: float = 0.0, so2: float = 0.0, co: float = 0.0) -> Tuple[int, AQICategory, str]:
    """Calculates aggregated NAQI index taking the maximum sub-index as lead pollutant."""
    sub_pm25 = calculate_sub_index(pm25, BREAKPOINTS_PM25)
    sub_pm10 = calculate_sub_index(pm10, BREAKPOINTS_PM10)
    sub_no2 = calculate_sub_index(no2, BREAKPOINTS_NO2) if no2 > 0 else 0
    
    pollutants = [
        ("PM2.5", sub_pm25),
        ("PM10", sub_pm10),
        ("NO2", sub_no2)
    ]
    primary_pollutant, max_aqi = max(pollutants, key=lambda x: x[1])
    category = get_category_from_aqi(max_aqi)
    return max_aqi, category, primary_pollutant

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance in kilometers."""
    r = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

class AQIEngine:
    """Main AQI Telemetry and Spatial Interpolation Engine."""
    
    def __init__(self):
        self._stations: Dict[str, AirQualityStation] = {}
        self._load_seed_stations()
        
    def _load_seed_stations(self):
        # Official Delhi NCR CPCB Monitoring Stations around Delhi/DTU
        seed_data = [
            ("DL-DTU-01", "DTU Bawana / Shahbad Daulatpur", "Delhi", "Delhi", 28.7499, 77.1170, 245.0, 380.0, 68.0, 18.0, 2.1),
            ("DL-JHN-02", "Jahangirpuri Industrial Area", "Delhi", "Delhi", 28.7328, 77.1706, 295.0, 430.0, 85.0, 24.0, 2.8),
            ("DL-ROH-03", "Rohini Sector 16", "Delhi", "Delhi", 28.7325, 77.1199, 210.0, 340.0, 55.0, 15.0, 1.9),
            ("DL-ANV-04", "Anand Vihar ISBT", "Delhi", "Delhi", 28.6469, 77.3160, 360.0, 480.0, 110.0, 32.0, 3.9),
            ("DL-PNB-05", "Punjabi Bagh", "Delhi", "Delhi", 28.6683, 77.1167, 195.0, 310.0, 62.0, 19.0, 1.8),
            ("DL-RKP-06", "R.K. Puram", "Delhi", "Delhi", 28.5660, 77.1767, 180.0, 290.0, 48.0, 14.0, 1.5),
            ("DL-MDM-07", "Mandir Marg (Central Ridge)", "Delhi", "Delhi", 28.6360, 77.2010, 145.0, 230.0, 38.0, 11.0, 1.2),
            ("DL-DWK-08", "Dwarka Sector 8", "Delhi", "Delhi", 28.5710, 77.0710, 175.0, 280.0, 45.0, 13.0, 1.4),
            ("DL-NOI-09", "Noida Sector 62", "Noida", "Uttar Pradesh", 28.6270, 77.3620, 230.0, 360.0, 72.0, 20.0, 2.0),
            ("DL-GUR-10", "Gurugram Cyber City / DLF", "Gurugram", "Haryana", 28.4900, 77.0900, 190.0, 305.0, 58.0, 16.0, 1.7),
        ]
        
        for sid, name, city, state, lat, lon, pm25, pm10, no2, so2, co in seed_data:
            aqi, cat, _ = calculate_cpcb_aqi(pm25, pm10, no2, so2, co)
            station = AirQualityStation(
                station_id=sid,
                name=name,
                city=city,
                state=state,
                latitude=lat,
                longitude=lon,
                pm25=pm25,
                pm10=pm10,
                no2=no2,
                so2=so2,
                co=co,
                aqi=aqi,
                category=cat
            )
            self._stations[sid] = station

    def get_all_stations(self) -> List[AirQualityStation]:
        return list(self._stations.values())

    def get_station_by_id(self, station_id: str) -> Optional[AirQualityStation]:
        return self._stations.get(station_id)

    def add_or_update_station(self, station: AirQualityStation):
        self._stations[station.station_id] = station

    def estimate_hyperlocal_aqi(self, lat: float, lon: float, power: float = 2.0) -> Dict[str, Any]:
        """
        Calculates exact interpolated AQI and particulate matter at any lat/lon
        using Inverse Distance Weighting (IDW) interpolation from surrounding stations.
        """
        total_weight = 0.0
        weighted_aqi = 0.0
        weighted_pm25 = 0.0
        weighted_pm10 = 0.0
        
        nearest_station = None
        min_dist = float('inf')
        
        for station in self._stations.values():
            dist = haversine_distance(lat, lon, station.latitude, station.longitude)
            if dist < min_dist:
                min_dist = dist
                nearest_station = station
                
            # If coordinates are identical to an active station, return exact
            if dist < 0.05:
                return {
                    "latitude": lat,
                    "longitude": lon,
                    "estimated_aqi": station.aqi,
                    "category": station.category.value,
                    "pm25": station.pm25,
                    "pm10": station.pm10,
                    "confidence": "Exact Sensor Match",
                    "nearest_station": station.name,
                    "distance_km": round(dist, 2)
                }
            
            weight = 1.0 / (dist ** power)
            total_weight += weight
            weighted_aqi += station.aqi * weight
            weighted_pm25 += station.pm25 * weight
            weighted_pm10 += station.pm10 * weight

        final_aqi = int(round(weighted_aqi / total_weight))
        final_pm25 = round(weighted_pm25 / total_weight, 1)
        final_pm10 = round(weighted_pm10 / total_weight, 1)
        category = get_category_from_aqi(final_aqi)

        return {
            "latitude": lat,
            "longitude": lon,
            "estimated_aqi": final_aqi,
            "category": category.value,
            "pm25": final_pm25,
            "pm10": final_pm10,
            "confidence": "IDW Spatial Interpolation",
            "nearest_station": nearest_station.name if nearest_station else "Unknown",
            "distance_km": round(min_dist, 2)
        }
