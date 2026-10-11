// ==============================================================================
// VayuRakshak AI - Cedar Policy Definitions (AWS Open-Source Cedar Language)
// Author: Bhomesh Razdan (Lead Architect)
// Hackathon: Bharat Builds Tour - Environmental Hacks (WeMakeDevs x AWS)
// ==============================================================================

// Policy 1: Public Citizen Telemetry Access
// Permits any authenticated or public user to view AQI telemetry, plan clean corridors, and fetch health advisories
permit (
    principal in VayuRakshak::Role::"Citizen",
    action in [
        VayuRakshak::Action::"ViewAQI",
        VayuRakshak::Action::"PlanCleanRoute",
        VayuRakshak::Action::"GetHealthAdvisory",
        VayuRakshak::Action::"ReportIncident"
    ],
    resource
);

// Policy 2: School Safety Governance
// Permits verified school principals to broadcast emergency closure & safety advisories
permit (
    principal in VayuRakshak::Role::"SchoolPrincipal",
    action in [
        VayuRakshak::Action::"BroadcastSchoolAdvisory",
        VayuRakshak::Action::"TriggerRemoteClasses",
        VayuRakshak::Action::"ViewAQI",
        VayuRakshak::Action::"PlanCleanRoute"
    ],
    resource is VayuRakshak::Resource::"SchoolSafetyProtocol"
);

// Policy 3: Municipal Clean Air Enforcement
// Permits municipal environmental officers to declare GRAP emergency stages and deploy anti-smog equipment
permit (
    principal in VayuRakshak::Role::"MunicipalOfficer",
    action in [
        VayuRakshak::Action::"DeclareGRAPEmergency",
        VayuRakshak::Action::"DispatchAntiSmogGun",
        VayuRakshak::Action::"HaltConstruction"
    ],
    resource is VayuRakshak::Resource::"MunicipalAction"
);

// Policy 4: Platform Administrator Full Access
permit (
    principal in VayuRakshak::Role::"Admin",
    action,
    resource
);
