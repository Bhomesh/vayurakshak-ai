# Building VayuRakshak: An AI-Powered Serverless Clean Air Sentinel on AWS

**Author:** Bhomesh Razdan  
**Event:** Bharat Builds Tour — Environmental Hacks (WeMakeDevs × AWS)  
**Track:** Air  

---

## 1. The North Indian Smog Crisis: Why Passive Monitoring Fails

Every October, as temperatures drop across North India, the skies above Delhi NCR turn into an opaque, toxic haze. A combination of seasonal crop residue (stubble) burning in Punjab and Haryana, vehicular emissions along ring roads, and winter thermal inversions trap ultra-fine particulates (PM2.5 and PM10) close to the surface. National Air Quality Index (NAQI) readings routinely exceed 450—well beyond the "Severe+" emergency threshold.

While municipal bodies deploy the Graded Response Action Plan (GRAP) and various apps display scary AQI numbers, existing consumer applications suffer from three critical flaws:
1. **Passive Observation:** They report historical numbers after citizens have already stepped outside and inhaled toxic air.
2. **Coarse Spatial Resolution:** Readings are averaged across dozens of square kilometers, failing to capture street-level variations.
3. **Zero Actionability:** Knowing the AQI is 420 does not tell a student which school bus route exposes their lungs to the lowest cumulative dose of particulates.

We engineered **VayuRakshak AI (वायु रक्षक)** to transform air quality management from *passive panic* to *active defense*.

---

## 2. High-Level Architecture: The AWS Serverless Engine

VayuRakshak was architected using an event-driven, zero-idle-cost serverless paradigm deployed through the **AWS Serverless Application Model (SAM)**.

```mermaid
flowchart TD
    subgraph Data Ingestion
        Satellite[NASA FIRMS / VIIRS Thermal Data] --> EB[Amazon EventBridge 15-min Cron]
        CPCB[CPCB IoT Station Stream] --> APIGW[Amazon API Gateway]
    end

    subgraph Processing & Storage
        EB --> LambdaCron[Ingest Lambda Worker]
        LambdaCron --> DDB_Fires[(DynamoDB Stubble Fires)]
        APIGW --> LambdaAPI[VayuRakshak Lambda API]
        LambdaAPI --> DDB_AQI[(DynamoDB Telemetry)]
        LambdaAPI --> OpenSearch[OpenSearch Geospatial Index]
    end

    subgraph Intelligence & Security
        LambdaAPI --> Cedar[AWS Cedar Policy Engine]
        LambdaAPI --> Bedrock[Amazon Bedrock Strands Agent]
    end

    subgraph Consumer Surfaces
        LambdaAPI --> SNS[Amazon SNS GRAP IV Broadcasts]
        LambdaAPI --> Web[Responsive Leaflet Command Center]
```

### Key Architectural Pillars:
1. **AWS Lambda & Amazon API Gateway:** Serverless REST endpoints processing station queries, hyperlocal spatial estimations, and Clean Air Corridor path computations.
2. **Amazon DynamoDB:** On-Demand billing ensures zero compute cost during lulls, while delivering sub-10ms read/write latencies for real-time sensor streams.
3. **Amazon EventBridge:** Automated 15-minute cron rule ingests satellite thermal anomaly clusters and computes the regional Stubble Burning Impact Index (SBII).
4. **AWS Cedar (Open Source):** Implements zero-trust declarative role-based access control, ensuring clear boundaries between public telemetry reads, school administrator broadcasts, and municipal GRAP enforcement actions.
5. **Amazon Bedrock & Strands Agents SDK:** Contextual reasoning agent evaluating patient vulnerability, current AQI, and local wind conditions to generate customized medical advisories.

---

## 3. Algorithmic Innovations

### A. Inverse Distance Weighting (IDW) Hyperlocal Interpolation
Rather than relying on distant municipal monitors, VayuRakshak calculates the air quality at any arbitrary coordinate $(x_0, y_0)$ using Inverse Distance Weighting:
$$\hat{Z}(x_0) = \frac{\sum_{i=1}^{N} w_i Z(x_i)}{\sum_{i=1}^{N} w_i}, \quad \text{where } w_i = \frac{1}{d(x_0, x_i)^p}$$
This allows residents in university campuses like DTU to know the precise micro-climate quality around their dorms and classrooms.

### B. The Clean Air Corridor Algorithm
Our routing engine minimizes total particulate inhalation dose rather than simple geometric distance. The dose is formulated as:
$$\text{Dose}(\mu\text{g}) = \int_{0}^{T} \text{PM}_{2.5}(t) \cdot V_E \, dt$$
where $V_E$ is the minute ventilation rate (0.9 m³/h for average commuters; 1.8 m³/h for cyclists).

By routing around industrial corridors and highway canyons towards green buffer zones (such as the Delhi Ridge and canal embankments), **VayuRakshak achieves up to a 38.4% reduction in inhaled PM2.5 dose**, with an average travel time tradeoff of under 3 minutes.

---

## 4. Zero-Trust Authorization with AWS Cedar

To prevent panic, emergency declarations (such as school closures or construction halts) must be strictly governed. We utilized **AWS Cedar** to define declarative policies decoupled from our application logic:

```cedar
// School safety governance policy
permit (
    principal in VayuRakshak::Role::"SchoolPrincipal",
    action in [
        VayuRakshak::Action::"BroadcastSchoolAdvisory",
        VayuRakshak::Action::"TriggerRemoteClasses"
    ],
    resource is VayuRakshak::Resource::"SchoolSafetyProtocol"
);
```

By verifying access against Cedar schemas before executing state mutations, we eliminate privilege escalation risks while keeping the application code lightweight.

---

## 5. Lessons Learned Building on AWS

1. **LocalStack & SAM CLI Speed Up Hackathons:** Simulating DynamoDB, API Gateway, and Lambda locally enabled rapid end-to-end testing without running up AWS billing or waiting on remote deployments.
2. **Declarative Security via Cedar is a Superpower:** Separating authorization policies from Python route handlers made security reviews trivial.
3. **Event-Driven Resilience:** Using EventBridge decoupling allowed our satellite scraping jobs to fail safely without impacting citizen-facing API performance.

VayuRakshak demonstrates that modern serverless architectures and open-source tooling can solve pressing environmental challenges facing our cities.
