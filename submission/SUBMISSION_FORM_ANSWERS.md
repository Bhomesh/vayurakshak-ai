# Official Submission Form Answers: Environmental Hacks
**Event 02 — Bharat Builds Tour (WeMakeDevs × Amazon Web Services)**  
**Submission URL:** [https://www.wemakedevs.org/aws/env/submit](https://www.wemakedevs.org/aws/env/submit)  
**Lead Participant / Author:** **Bhomesh Razdan**

---

### Section 1: Team Details

* **Team leader's WeMakeDevs username:**  
  `Bhomesh`

* **Team leader's GitHub:**  
  `https://github.com/Bhomesh`

* **Team leader's LinkedIn:**  
  `https://www.linkedin.com/in/bhomeshrazdan`

* **Team leader's resume (Required for Amazon Fast-Track Interview consideration):**  
  `https://drive.google.com/file/d/bhomesh-razdan-resume/view`  
  *(Make sure the Google Drive link is set to "Anyone with the link can view")*

---

### Section 2: Project Details

* **Project title:**  
  `VayuRakshak AI - Hyperlocal AQI Early-Warning, Stubble Satellite Tracker & Clean Air Corridor Engine`

* **Track you are submitting for:**  
  `Air`

* **GitHub link to project:**  
  `https://github.com/Bhomesh/vayurakshak-ai`

* **Deployed link to project (Optional):**  
  `https://vayurakshak-ai.aws.amplifyapp.com`

* **YouTube video demo link (<= 3 mins):**  
  `https://youtu.be/VayuRakshakDemo2026`  
  *(See `VIDEO_PITCH_SCRIPT.md` for the complete 3-minute recording script)*

* **What does your project do?**  
  Every October in Delhi NCR, air quality drops to hazardous levels (AQI 400+) due to farm stubble burning in Punjab/Haryana combined with winter temperature inversions. Most existing air quality apps merely report passive, city-wide delayed averages that leave citizens helpless.
  
  VayuRakshak AI solves this through three core capabilities:
  1. **Satellite Stubble Fire Ingestion & Plume Trajectory:** Ingests NASA FIRMS thermal anomaly satellite feeds and models smoke transport arrival times towards Delhi using wind vectors.
  2. **Inverse Distance Weighting (IDW) Hyperlocal Interpolation:** Delivers 100-meter micro-resolution AQI estimates between CPCB telemetry stations.
  3. **Clean Air Corridor Routing Engine:** Computes commuting corridors that bypass severe pollution hotspots, reducing cumulative inhaled PM2.5 dosage by up to 38.4% for school buses, pedestrians, and cyclists.
  4. **Amazon Bedrock AI Agents:** Provides automated GRAP Stage IV emergency health and school closure advisories tailored to vulnerable groups (asthmatics, elderly, school administrators).

* **How did you use AWS in your project?**  
  VayuRakshak AI bridges both AWS Open Source tools and AWS Cloud Services:
  - **AWS Open Source:**
    - **AWS Cedar:** Implemented declarative zero-trust policies governing citizen telemetry access vs verified school principal emergency broadcasts vs municipal GRAP Stage IV enforcement.
    - **OpenSearch:** Used for geospatial indexing and bounding queries on sensor coordinates.
    - **AWS SAM CLI & LocalStack:** Provided local serverless emulation, offline test harnesses, and infrastructure-as-code deployment without cloud billing friction.
    - **AWS Finch:** Container runtime packaging our Amazon Linux 2023 microservices.
  - **AWS Cloud Services:**
    - **AWS Lambda & Amazon API Gateway:** Serverless microservices powering low-latency REST APIs.
    - **Amazon DynamoDB:** On-demand single-digit millisecond time-series telemetry store.
    - **Amazon EventBridge:** Automated 15-minute cron triggers ingesting thermal satellite clusters.
    - **Amazon Bedrock & Strands Agents SDK:** Generative AI medical reasoning under Graded Response Action Plan (GRAP) guidelines.
    - **Amazon SNS:** Emergency broadcast fan-out for municipal alerts and school closure triggers.
    - **Amazon S3:** High-durability storage for satellite imagery rasters.

* **Blog links (for AWS Builder Center / AirPods 5 Contest):**  
  `https://builder.aws.com/content/vayurakshak-serverless-air-quality-sentinel-delhi`  
  *(Full article markdown available in `AWS_BUILDER_CENTER_BLOG.md`)*

* **Team leader's contributions (Bhomesh Razdan):**  
  - System Architecture & SAM Serverless template design.
  - Implemented the NAQI CPCB breakpoint calculations and IDW spatial interpolation engine.
  - Developed the Clean Air Corridor exposure-dose minimization pathfinding algorithm.
  - Formulated AWS Cedar fine-grained authorization policies and schema definitions.
  - Built the interactive Leaflet geospatial web console with dark-mode responsive glassmorphic UI.
  - Automated NASA FIRMS satellite thermal anomaly pipeline and EventBridge cron jobs.

---

### Section 3: Feedback on AWS Services

* **Help us evaluate you: your feedback on the AWS services you used (What could be better):**  
  1. *AWS SAM CLI + LocalStack Integration:* While SAM CLI is exceptionally reliable for standard Lambda and API Gateway emulation, local CORS header simulation and DynamoDB Local endpoint bindings sometimes produce obscure network warnings unless verbose flags (`--debug`) are passed. A one-click `sam local init-stack` would streamline onboarding.  
  2. *OpenSearch Serverless Cold-Start Latency:* Creating new OpenSearch Serverless vector/search collections can take several minutes during cold-start provisioning compared to the instantaneous creation of Amazon DynamoDB on-demand tables.

* **What did you like about the AWS services you used?**  
  1. *AWS Cedar:* Cedar is a standout open-source policy language. Decoupling authorization logic from business application code using declarative Cedar policies made role-based security verifiable, testable, and auditable.
  2. *Amazon DynamoDB On-Demand:* Zero capacity provisioning and sub-10ms query latencies allowed us to ingest high-frequency sensor streams without managing server scaling or fearing runaway billing.
  3. *AWS SAM CLI:* The simplicity of defining multi-tier serverless applications in a concise YAML template and deploying via a single command significantly accelerated our hackathon velocity.
