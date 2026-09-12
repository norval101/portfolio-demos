<div align="center">

# Norval Mendez | Systems Architecture & Engineering Portfolio

**Senior Software Developer & Lead Systems Architect**  
*Windsor, ON, Canada • [LinkedIn](https://www.linkedin.com/in/norval-mendez-369a2611a) • [Portfolio](https://norvalmendez.ca) • [Email](mailto:norvalmendez.ca@gmail.com)*

[![GitHub Profile](https://img.shields.io/badge/GitHub-norval101-181717?style=flat&logo=github)](https://github.com/norval101)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Norval_Mendez-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/norval-mendez-369a2611a)
[![Portfolio](https://img.shields.io/badge/Website-norvalmendez.ca-0052CC?style=flat&logo=googlechrome)](https://norvalmendez.ca)
[![Tests Passing](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen?style=flat&logo=checkmarx)](https://github.com/norval101/portfolio-demos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <b>High-Availability Cloud Systems • RESTful Microservices & APIs • AI Automated Screening Pipelines • Enterprise Architecture</b>
</p>

---

</div>

## 📌 Executive Summary & Architecture Showcase

I am an award-winning **Senior Software Developer & Systems Architect** with 8+ years of engineering leadership, designing mission-critical SaaS platforms, cloud infrastructure (AWS/GCP), and distributed backend architectures.

Throughout my career, I have:
- **Architected high-availability systems for 8,000+ global users**, sustaining 99.9% uptime and powering 400% YoY enterprise revenue growth.
- **Pioneered automated AI vetting & audit pipelines**, slashing cross-border applicant rejection rates by **94%**.
- **Standardized partner REST integration specifications**, cutting B2B onboarding lead time by **87%** and operational latency by **85%**.
- **Built acquisition-ready platforms**, including the core distribution logistics system for *GK Campus Connect*, directly prompting enterprise acquisition by the **Grace Kennedy Group**.

---

## 🔒 Confidentiality & NDA Provenance Notice

> **Why are some production repositories private?**  
> Many of the platforms detailed below process proprietary enterprise data, cross-border workforce documents, commercial logistics, or client financial workflows protected under strict Non-Disclosure Agreements (NDAs).
>
> To respect client confidentiality while providing hiring managers and technical leadership with complete visibility into my architectural thinking, this repository provides:
> 1. **Production System Architecture Blueprints** (rendered via Mermaid.js directly in GitHub).
> 2. **Technical Specifications & Problem-Solving Deconstructions** (trade-offs, bottlenecks, data flow, security governance).
> 3. **Public Sandbox Code Implementations** (clean code patterns, unit test coverage, and API contracts demonstrating my coding standards).

---

## 🗺️ System Architecture Gallery

### 1. WATSOF — Global Cloud-Native Workforce SaaS & Automated AI Audit Engine
**Role:** Lead Technical Product Manager & Systems Architect (JELPO Group)  
**Scale:** 8,000+ Global Users | Multi-Region AWS & GCP | 99.9% SLA

#### Business Context & Challenge
The platform manages high-volume international exchange and workforce candidate processing. Manual vetting caused severe bottlenecks, documentation errors, high sponsor rejection rates, and cross-border latency issues across North America and the Caribbean.

#### Architectural Solution
- Architected a multi-region cloud topology leveraging AWS/GCP with Cloudflare edge caching, cutting global end-user latency by **85%**.
- Implemented an asynchronous event-driven document validation pipeline using AI pre-screening algorithms to detect anomalies, missing certifications, and compliance errors prior to sponsor submission.
- Standardized B2B webhook APIs, reducing enterprise partner onboarding from weeks to days (**87% reduction**).

```mermaid
flowchart TD
    subgraph Clients["Global Client Layer"]
        A1["Web Application (SPA / React / PHP)"]
        A2["Partner B2B Systems (REST APIs)"]
        A3["Mobile Clients (Candidate Onboarding)"]
    end

    subgraph Edge["Global CDN & Edge Routing"]
        CF["Cloudflare Edge Network / WAF"]
        ALB["Application Load Balancers (Multi-Region)"]
    end

    subgraph AppCluster["Core Services (Containerized VPC)"]
        SVC_AUTH["OAuth2 / JWT Auth Service"]
        SVC_APP["Application Core Gateway"]
        SVC_PARTNER["B2B Webhook & Partner Integration Engine"]
    end

    subgraph AsyncPipeline["Asynchronous Processing & AI Audit"]
        Q["Message Broker (Redis Queue / Event Bus)"]
        W1["Candidate Vetting Worker"]
        W2["AI Audit & Document Validation Engine"]
        W3["Notification & Dispatch Engine"]
    end

    subgraph Persistence["Data & Object Storage Tier"]
        DB[(Multi-AZ MySQL Cluster - Normalized Schema)]
        CACHE[(Redis Cluster - Session & Query Caching)]
        S3[(Encrypted Document Store / S3 / GCS)]
    end

    Clients --> CF
    CF --> ALB
    ALB --> SVC_AUTH
    ALB --> SVC_APP
    ALB --> SVC_PARTNER

    SVC_APP --> CACHE
    SVC_APP --> DB
    SVC_APP --> Q

    Q --> W1
    Q --> W2
    Q --> W3

    W2 --> S3
    W2 --> DB
    W2 -.->|"Audit Verification Passed (94% Rejection Drop)"| SVC_PARTNER
```

#### Key Engineering Metrics & Outcomes
- **-94%** cross-border processing rejection rate via automated compliance vetting.
- **-85%** global end-user latency using multi-region edge distribution.
- **-87%** partner onboarding time using OpenAPI-standardized REST endpoints.
- **99.9%** availability maintained across 8,000+ active enterprise users.

---

### 2. LMIAPro — Candidate Vetting & Workforce Matching Engine
**Role:** Lead Systems Architect & Product Manager (LMIAPro — Calgary, AB)  
**Tech:** PHP, RESTful APIs, MySQL, Redis, Asynchronous Workers

#### Business Context & Challenge
Canadian employers faced prolonged recruitment cycles when seeking qualified international personnel under regulatory compliance constraints. Candidate tracking systems were fragmented, causing delayed vetting, mismatched qualifications, and manual interview coordination.

#### Architectural Solution
- Designed and built a bespoke candidate tracking CRM and algorithmic matching engine from scratch.
- Implemented a two-sided matching algorithm that maps employer role requirements (experience level, NOC classifications, skill tags) against candidate verification scores.
- Automated end-to-end recruitment pipelines including interview scheduling, status transitions, and compliance audit trail generation.

```mermaid
flowchart LR
    subgraph Ingestion["Talent Ingestion & Employer Needs"]
        CAND["Candidate Application Portal"]
        EMP["Employer Job Requisition Intake"]
    end

    subgraph ScoringEngine["Vetting & Matching Engine"]
        EXTRACT["Data Normalization & Parser"]
        RULES["Regulatory Rules & Eligibility Validator"]
        MATCHER["Weighted Multi-Criteria Matching Engine"]
    end

    subgraph Workflow["Automated Pipeline & Notifications"]
        SCHED["Interview Auto-Scheduler"]
        AUDIT["Immutable Audit Trail & Status Ledger"]
        NOTIF["Real-time Notification & Webhook Dispatch"]
    end

    subgraph Storage["Persistent Layer"]
        CORE_DB[(Normalized Database - Candidates, Jobs, Placements)]
        SEARCH_CACHE[(Search Index / Redis Cache)]
    end

    CAND --> EXTRACT
    EMP --> EXTRACT
    EXTRACT --> RULES
    RULES --> MATCHER
    MATCHER <--> SEARCH_CACHE
    MATCHER --> CORE_DB
    MATCHER --> SCHED
    SCHED --> NOTIF
    SCHED --> AUDIT
    AUDIT --> CORE_DB
```

#### Key Engineering Metrics & Outcomes
- Automated candidate tracking workflows from entry to exit with zero data-entry duplication.
- Drastically accelerated employer-candidate matching times and interview scheduling.
- Implemented rigorous database constraints to ensure full regulatory auditability.

---

### 3. Real-Time Operations Dispatch & Field Communication Infrastructure
**Role:** Business Systems Support Specialist (Mango Maids — Calgary, AB)  
**Tech:** Real-time WebSockets, VoIP Systems, RESTful Dispatch API, MySQL

#### Business Context & Challenge
High-density field operations required responsive real-time dispatching, rapid cleaner scheduling, instant customer support resolution, and resilient VoIP communications to prevent missed appointments and operational bottlenecks.

#### Architectural Solution
- Built and integrated an automated operations engine for field cleaner scheduling and dispatch routing.
- Deployed a low-latency real-time live chat customer support pipeline to increase client engagement and response speed.
- Re-engineered VoIP routing topologies, resolving communication drops and unifying customer interaction channels into the internal management platform.

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Client / Support User
    participant WebApp as Web / LiveChat Portal
    participant API as Dispatch & Communication API
    participant VoIP as VoIP Telephony Gateway
    participant DB as Operations Database
    actor FieldStaff as Field Service Cleaner

    Customer->>WebApp: Initiates Live Chat / Service Booking
    WebApp->>API: Dispatches Event (WebSocket / REST)
    API->>DB: Stores Job Record & Computes Nearest Route
    API->>FieldStaff: Push Notification: Job Assignment & Schedule
    FieldStaff-->>API: Confirms Dispatch Acceptance
    API->>Customer: Real-Time Confirmation & ETA Alert
    opt Voice Support Escalation
        Customer->>VoIP: Customer Calls Inbound
        VoIP->>API: Webhook: Lookup Customer History
        API-->>VoIP: Route to Dedicated Agent with Context
    end
```

---

### 4. GK Campus Connect — Food Bank Distribution Logistics Platform
**Role:** Technical Co-Founder & Distribution Specialist  
**Acquisition:** Acquired by **Grace Kennedy Group**  
**Scale:** Biweekly food package delivery to 1,000+ university students

#### Business Context & Challenge
Legacy distribution relied on error-prone paper records and ad-hoc spreadsheets, causing inventory discrepancies, lack of traceability, and inability to report verified metrics to corporate sponsors.

#### Architectural Solution
- Directed the database schema normalization and domain modeling to transition manual distribution into a high-availability digital inventory and recipient management software.
- Authored UML specifications, data lineage mapping docs, and User Acceptance Testing (UAT) frameworks.
- Built an immutable custody-tracking distribution workflow that proved operational viability, winning corporate confidence and resulting in full enterprise acquisition by **Grace Kennedy Group**.

```mermaid
flowchart TD
    DONOR["Donors & Corporate Sponsors"] -->|Supply Consignments| WAREHOUSE["Inventory Ingestion & Batch Tagging"]
    WAREHOUSE -->|Serialized Batches| DB[(Normalized Logistics Database)]
    
    STUDENT["Student Beneficiary Identification"] -->|Eligibility Verification| AUTH_GATE["Identity & Allocation Gate"]
    AUTH_GATE --> DB
    
    DISPATCH["Biweekly Distribution Stations"] -->|Real-Time Barcode / ID Scan| CHECKOUT["Allocation Ledger & Chain-of-Custody"]
    CHECKOUT --> DB
    
    DB --> AUDIT_REPORT["Automated Reporting & Lineage Proofs"]
    AUDIT_REPORT -->|Validated Audit Logs| ACQ["Enterprise Due Diligence & Acquisition (Grace Kennedy)"]
```

---

## 💻 Tech Stack & Technical Competencies

| Domain | Technologies & Frameworks |
| :--- | :--- |
| **Languages** | PHP, Python, JavaScript/TypeScript, Java, C#, C++, SQL, HTML5, CSS3, Flutter |
| **Backend & Architecture** | Systems Architecture, Microservices, RESTful APIs, OOP / SOLID, MVC, Webhooks, GraphQL |
| **Databases & Caching** | MySQL (Complex Joins, Index Optimization, Normalization), Redis, PostgreSQL |
| **Cloud & DevOps** | AWS (EC2, S3, RDS, CloudFront), Google Cloud Platform (GCP), Docker, CI/CD Pipelines, Git/GitHub |
| **Security & Auth** | OAuth 2.0, Auth0, JWT Authentication, RBAC (Role-Based Access Control), Data Privacy Governance |
| **Testing & Quality** | Unit Testing (PHPUnit, Jest, PyTest), Integration Testing, UAT Test Plans, Rigorous Code Review |
| **Modern Tooling** | Agentic AI Workflows (Cursor, Claude Code), Custom Python Diagnostics, Jira, Agile/Scrum |

---

## 🏆 Awards & Industry Honors

- 🥇 **Top Innovator of the Year (2024)** — *Ministry of Labour & Social Security (Jamaica)*
- 🏅 **DBJ IGNITE Innovation Award (2022)** — *Development Bank of Jamaica*
- 🏆 **Entrepreneurship & Innovation Award (2016)** — *University of the West Indies*
- 🎓 **UML & Software Design Certification (2022)** — *University of Alberta*
- 🔐 **Computer Network Systems & Security (2021)** — *University of Colorado*

---

## 📁 Functional Sandbox Demos (Included in this Repo)

To complement the architectural blueprints above, two fully tested, self-contained reference sandboxes are implemented directly within this repository:

### 1. [`demos/workforce-matching-engine/`](./demos/workforce-matching-engine)
- **Concept:** Production-grade two-sided candidate matching engine & regulatory eligibility gate (inspired by the LMIAPro architecture).
- **Features:** Clean OOP domain architecture, weighted scoring algorithm, tamper-evident SHA-256 chained audit ledger, built-in REST API server, and OpenAPI 3.0 specification.
- **Run Unit Tests:**
  ```bash
  python -m unittest discover -s demos/workforce-matching-engine/tests -t demos/workforce-matching-engine -p "test_*.py" -v
  ```

### 2. [`demos/document-audit-pipeline/`](./demos/document-audit-pipeline)
- **Concept:** Multi-stage automated document audit and risk scoring engine (inspired by the WATSOF compliance pipeline that reduced rejection rates by 94%).
- **Features:** Format & checksum verification, temporal validity & expiration boundary checking, token-based identity consistency matching, and regulatory compliance rules.
- **Run Unit Tests:**
  ```bash
  python -m unittest discover -s demos/document-audit-pipeline/tests -t demos/document-audit-pipeline -p "test_*.py" -v
  ```

---

## 🧪 Run All Repository Tests
```bash
# Run both test suites simultaneously from root (zero external dependencies required)
python -m unittest discover -s demos/workforce-matching-engine/tests -t demos/workforce-matching-engine -p "test_*.py"
python -m unittest discover -s demos/document-audit-pipeline/tests -t demos/document-audit-pipeline -p "test_*.py"
```

---

## 📬 Contact & Connect

- **Website:** [norvalmendez.ca](https://norvalmendez.ca)
- **LinkedIn:** [linkedin.com/in/norval-mendez-369a2611a](https://www.linkedin.com/in/norval-mendez-369a2611a)
- **Email:** [norvalmendez.ca@gmail.com](mailto:norvalmendez.ca@gmail.com) / [norval@digitalawah.com](mailto:norval@digitalawah.com)
- **Location:** Windsor, ON, Canada
