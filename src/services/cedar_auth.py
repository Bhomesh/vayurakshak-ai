"""
VayuRakshak AI - AWS Cedar Policy & Fine-Grained Authorization Engine
Open-Source Tool: AWS Cedar (Cedar Policy Language)
Evaluates principal, action, resource, and context against declarative security policies.
Author: Bhomesh Razdan (Lead Architect)
"""

from typing import Dict, Any, Tuple

class CedarPolicyEngine:
    """Evaluates fine-grained authorization policies matching AWS Cedar semantics."""

    def __init__(self):
        self.policies = [
            # Policy 1: Any citizen can view public telemetry and request clean routes
            {
                "id": "policy::permit_citizen_read",
                "effect": "permit",
                "principal_roles": ["Citizen", "SchoolPrincipal", "MunicipalOfficer", "Admin"],
                "actions": ["Action::ViewAQI", "Action::PlanCleanRoute", "Action::GetHealthAdvisory", "Action::ReportIncident"],
                "resource_types": ["Telemetry", "Route", "Advisory", "CitizenReport"]
            },
            # Policy 2: Only SchoolPrincipals and Admins can broadcast school advisories
            {
                "id": "policy::permit_school_broadcast",
                "effect": "permit",
                "principal_roles": ["SchoolPrincipal", "Admin"],
                "actions": ["Action::BroadcastSchoolAdvisory", "Action::TriggerRemoteClasses"],
                "resource_types": ["SchoolSafetyProtocol"]
            },
            # Policy 3: Only MunicipalOfficers and Admins can enforce GRAP emergency mandates
            {
                "id": "policy::permit_municipal_enforcement",
                "effect": "permit",
                "principal_roles": ["MunicipalOfficer", "Admin"],
                "actions": ["Action::DeclareGRAPEmergency", "Action::DispatchAntiSmogGun", "Action::HaltConstruction"],
                "resource_types": ["MunicipalAction"]
            }
        ]

    def is_authorized(self, principal_role: str, action: str, resource_type: str, context: Dict[str, Any] = None) -> Tuple[bool, str]:
        """
        Cedar authorization decision evaluator.
        Returns (is_allowed, policy_id_or_reason).
        Default behavior in Cedar: Explicit Permit required, Default Deny.
        """
        for policy in self.policies:
            if (policy["effect"] == "permit" and
                principal_role in policy["principal_roles"] and
                action in policy["actions"] and
                resource_type in policy["resource_types"]):
                return True, f"PERMIT by {policy['id']}"
                
        return False, f"DENY: No matching permit policy in Cedar store for {principal_role} invoking {action} on {resource_type}"
