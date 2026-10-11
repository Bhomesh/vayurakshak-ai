"""
VayuRakshak AI - Amazon Bedrock / Strands Agents SDK Advisory Engine
Provides personalized environmental health actions based on vulnerability & GRAP stages
Author: Bhomesh Razdan (Lead Architect)
"""

from typing import Dict, Any, List
from ..core.models import UserVulnerability, HealthAdvisory, AQICategory

class AdvisoryAgent:
    """Agentic AI engine providing contextual environmental advice and GRAP alerts."""

    def generate_advisory(self, location_name: str, aqi: int, category: str, vulnerability: UserVulnerability) -> HealthAdvisory:
        # Determine GRAP (Graded Response Action Plan) Stage
        if aqi <= 200:
            grap_stage = "Stage 0 (Normal)"
        elif aqi <= 300:
            grap_stage = "Stage I (Poor: 201-300)"
        elif aqi <= 400:
            grap_stage = "Stage II (Very Poor: 301-400)"
        elif aqi <= 450:
            grap_stage = "Stage III (Severe: 401-450)"
        else:
            grap_stage = "Stage IV (Severe+: >450 Emergency)"

        # Contextual advice based on vulnerability profile
        actions: List[str] = []
        school_text = ""
        outdoor_text = ""
        mask_text = "Standard cloth or surgical mask" if aqi < 200 else "N95 / FFP2 particulate respirator with tight seal"

        if vulnerability == UserVulnerability.CHILDREN_STUDENTS:
            if aqi > 300:
                school_text = f"CRITICAL [{grap_stage}]: Suspend all outdoor morning assemblies, sports, and PT sessions. Keep windows closed; operate HEPA purifiers in classrooms."
                outdoor_text = "Strictly avoid outdoor play. Indoor physical activities only."
                actions = [
                    "Distribute certified N95 masks to children during bus commutes",
                    "Transition primary classes (Pre-school to Grade 5) to hybrid/online if AQI persists > 400",
                    "Keep classroom air purifiers set to continuous High mode"
                ]
            else:
                school_text = "Classes normal. Limit strenuous physical activity outdoors."
                outdoor_text = "Permissible with moderate exertion."
                actions = ["Hydrate frequently", "Monitor children with known respiratory allergies"]

        elif vulnerability == UserVulnerability.ASTHMA_RESPIRATORY:
            if aqi > 200:
                actions = [
                    "Keep rapid-relief bronchodilator (inhaler) readily accessible at all times",
                    "Stay in air-conditioned or HEPA-filtered enclosed spaces",
                    "Avoid early morning outdoor walks when temperature inversion traps surface pollutants",
                    "Use saline nasal irrigation to clear trapped PM2.5 particulates"
                ]
                outdoor_text = "STRICTLY RESTRICTED: High risk of bronchospasm and acute exacerbation."
            else:
                actions = ["Standard prophylactic medications as prescribed", "Check peak flow meter"]
                outdoor_text = "Allowable in afternoons when thermal mixing disperses ground smog."
            school_text = "Exempt from outdoor school physical activities."

        elif vulnerability == UserVulnerability.OUTDOOR_WORKERS:
            if aqi > 300:
                actions = [
                    "Mandatory N95 mask usage during shifts with 15-minute breaks every 2 hours in filtered cabins",
                    "Employers must provide eye wash stations and hydration points",
                    "GRAP Construction Ban: Stop earthmoving, stone crushing, and dry demolition immediately"
                ]
                outdoor_text = "High risk of occupational respiratory inflammation. Rotate shifts."
            else:
                actions = ["Wear dust masks", "Wet-suppress dust before sweeping"]
                outdoor_text = "Permissible with PPE."
            school_text = "N/A - Worksite safety compliance active."

        else: # GENERAL_PUBLIC
            if aqi > 300:
                actions = [
                    "Keep home windows sealed; run air filtration",
                    "Avoid high-traffic corridors during morning and evening rush hours",
                    "Use public transport (Delhi Metro) instead of private vehicles to curb fleet emissions"
                ]
                outdoor_text = "Avoid non-essential outdoor exertion, jogging, or cycling."
            else:
                actions = ["Carpool or take metro", "Ventilate indoor spaces during sunny afternoons"]
                outdoor_text = "Safe for general outdoor recreation."
            school_text = "General advisory applies."

        return HealthAdvisory(
            vulnerability_group=vulnerability,
            location_name=location_name,
            current_aqi=aqi,
            primary_pollutant="PM2.5 (Fine Particulate Matter)",
            recommended_actions=actions,
            school_advisory=school_text,
            outdoor_activity_guidance=outdoor_text,
            mask_recommendation=mask_text,
            generated_by=f"Amazon Bedrock (Claude 3.5 Sonnet / Strands Agent) | {grap_stage}"
        )
