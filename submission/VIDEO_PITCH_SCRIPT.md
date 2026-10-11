# 3-Minute Video Pitch Script: VayuRakshak AI
**Event:** Bharat Builds Tour — Environmental Hacks (WeMakeDevs × AWS)  
**Speaker:** Bhomesh Razdan (Lead Architect)  
**Target Audience:** Hackathon Judges & Amazon University Talent Acquisition Team  
**Time Limit:** 3 Minutes Max (180 Seconds)

---

### [0:00 - 0:35] The Hook & Problem Statement (35 Seconds)
*(Visual: Screen shows Delhi smog headlines, followed by VayuRakshak live dashboard showing red AQI 388 at DTU Delhi)*

> **"Hello judges and the Amazon team! I am Bhomesh Razdan, and this is VayuRakshak AI.**
>
> Right now, in October across North India, the skies have turned into a toxic chamber. The Air Quality Index frequently crosses 400 into the Severe category due to winter temperature inversion and crop stubble burning across Punjab and Haryana.
>
> But here is the real issue: Every existing app only gives you a delayed city-wide number. If you are a school principal deciding whether to hold morning assembly, or a parent sending your child on a school bus, a scary number doesn't protect you.
>
> We built VayuRakshak AI to take us from **passive panic** to **active, hyperlocal environmental defense**."

---

### [0:35 - 1:20] Live Product Walkthrough & Core Features (45 Seconds)
*(Visual: Screen shares the interactive web console: Leaflet map showing CPCB stations, live satellite fire pins in Punjab, and Clean Air Corridor)*

> **"Here is VayuRakshak in action:**
>
> 1. **Live Satellite Fire Tracking:** Using NASA FIRMS thermal anomaly feeds, our system monitors 8 active stubble clusters in Punjab. By combining Fire Radiative Power with local wind vectors, we calculate the Stubble Burning Impact Index (SBII)—currently scoring 81 out of 100.
>
> 2. **Inverse Distance Weighting Interpolation:** We don't just rely on sparse sensors. Our spatial algorithm interpolates air quality down to 100-meter micro-coordinates across Delhi NCR.
>
> 3. **The Clean Air Corridor:** This is our most impactful feature. Look at this commute from DTU Bawana down to Connaught Place. The standard route takes high-congestion arterial roads with an AQI of 425, delivering 142 micrograms of toxic PM2.5 to your lungs.
>
> With one click, VayuRakshak calculates the Clean Air Corridor. By detouring around industrial bottlenecks and following vegetative green belts, **we cut the cumulative PM2.5 inhalation dose by 38.4%**, while adding less than 3 minutes to the commute!"

---

### [1:20 - 2:15] AWS Architecture & Open-Source Stack (55 Seconds)
*(Visual: Mermaid architecture diagram and code walkthrough showing template.yaml and Cedar policies)*

> **"Now, let's look at how we built this on AWS.**
>
> - **Build It (Open Source):**
>   - We integrated **AWS Cedar** for zero-trust authorization. Telemetry is public, but school closures and municipal GRAP Stage IV emergency declarations require cryptographically verified Cedar policy evaluation.
>   - We containerized using **AWS Finch** on Amazon Linux 2023, and ran our local test suite with **SAM CLI** and **LocalStack**.
>
> - **Ship It (AWS Cloud Native):**
>   - Our backend runs on **AWS Lambda** and **Amazon API Gateway** with sub-50ms execution times.
>   - High-throughput sensor streams are persisted in **Amazon DynamoDB** with On-Demand scaling, keeping idle costs at zero.
>   - **Amazon EventBridge** triggers our satellite ingestion worker every 15 minutes.
>   - And **Amazon Bedrock**, using Claude 3.5 and the Strands Agents framework, generates contextual medical advisories for asthmatics, outdoor workers, and schools under GRAP Stage IV."

---

### [2:15 - 3:00] Impact, Future Roadmap & Conclusion (45 Seconds)
*(Visual: Bhomesh on webcam / summary slide showing GitHub repo, zero-cost AWS deployment, and DTU build day relevance)*

> **"What fought back?** Tuning the multi-objective graph routing to balance distance penalties against particulate dose was challenging, but the result is a working system validated with 17 unit tests.
>
> VayuRakshak is built for the student walking to class at DTU, the school administrator safeguarding thousands of children, and the city planner allocating anti-smog water cannons.
>
> The code is fully open-source, tested, and ready for deployment.
>
> Thank you WeMakeDevs and AWS for this incredible Bharat Builds Tour experience. I'm Bhomesh Razdan—let's build what the planet needs!"

*(Visual: Displays GitHub repository URL `https://github.com/Bhomesh/vayurakshak-ai` and contact details)*
