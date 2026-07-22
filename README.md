# ⚡ ETAI — Energy Supply Chain Resilience Platform

> **AI-powered decision intelligence for resilient energy supply chains**

ETAI is an AI-driven Energy Supply Chain Resilience Platform designed to identify supply-chain risks, analyze their impact, simulate disruption scenarios, and generate explainable mitigation strategies.

The platform combines **Generative AI, Machine Learning, Retrieval-Augmented Generation (RAG), Knowledge Graphs, Digital Twin simulations, geospatial intelligence, and agentic AI orchestration** to demonstrate how critical energy supply chains can respond intelligently to geopolitical and operational disruptions.

---

## 🌐 Live Deployment

### Frontend — ETAI Dashboard

https://etai-energy-platform.onrender.com

### Backend — FastAPI Service

https://etai-hackathon.onrender.com

### GitHub Repository

https://github.com/prachi-01-ui/ETAI-Hackathon

> **Note:** The deployed system is a functional hackathon prototype, not a production-scale energy infrastructure system. It demonstrates the end-to-end architecture and decision-intelligence workflow using representative supply-chain data and scenarios.

---

# 🎯 Problem Statement

Energy supply chains are highly interconnected and increasingly vulnerable to:

- Geopolitical conflicts
- Maritime chokepoint disruptions
- Port congestion
- Sanctions
- Supplier failures
- Transportation delays
- Infrastructure disruptions
- Commodity and logistics risks

A disruption at one point in the network can propagate across suppliers, ports, shipping routes, refineries, inventories, procurement operations, and strategic reserves.

Traditional monitoring systems can identify risks, but decision-makers still need to determine:

- **What infrastructure will be affected?**
- **How severe will the impact be?**
- **What alternatives are available?**
- **Which mitigation strategy should be selected?**
- **What could be the operational outcome of that decision?**

ETAI addresses this gap by connecting **risk intelligence with prediction, simulation, knowledge retrieval, and AI-assisted decision making**.

---

# 💡 Our Solution

ETAI creates an intelligent representation of the energy supply chain and combines multiple analytical layers into a unified decision workflow.

```text
Risk Intelligence
        ↓
Knowledge Graph
        ↓
ML Risk Assessment
        ↓
Digital Twin Simulation
        ↓
RAG Knowledge Retrieval
        ↓
LangGraph AI Orchestration
        ↓
Gemini Decision Intelligence
        ↓
Recommendations & Actions
        ↓
Outcome Tracking
```

Instead of simply displaying a disruption, ETAI attempts to determine its operational consequences and recommend an appropriate mitigation strategy.

---

# ✨ Core Features

## 🚨 AI Risk Intelligence

The platform evaluates disruption events and generates structured risk assessments containing information such as:

- Risk score
- Severity
- Confidence score
- Verification status
- Recommended response
- Intervention probability

This transforms risk information into structured operational intelligence that can be passed to downstream AI and simulation components.

---

## 🧠 Agentic AI Decision Intelligence

ETAI uses **LangGraph** to orchestrate its AI decision workflow.

The workflow connects risk assessment with downstream decision generation:

```text
Risk Detection
      ↓
Risk Assessment
      ↓
ML Prediction
      ↓
Context Retrieval
      ↓
AI Decision Generation
      ↓
Mitigation Recommendation
```

The prototype demonstrates autonomous workflow progression where the risk assessment can determine whether further intervention and mitigation analysis are required.

---

## 🤖 Gemini-Powered Decision Agent

Google Gemini is integrated into the decision-intelligence layer to generate contextual mitigation strategies.

The AI Decision Agent can reason over information such as:

- Active risk events
- Affected supply-chain infrastructure
- Alternative routes
- Supplier capacity
- Refinery requirements
- Inventory conditions
- Scenario impact
- Estimated delays
- Financial impact

The generated recommendation includes an explanation of **why a particular mitigation strategy was selected**, improving transparency compared with a simple black-box recommendation.

---

## 📚 Retrieval-Augmented Generation (RAG)

ETAI uses a Retrieval-Augmented Generation workflow so that decision generation can incorporate project-specific supply-chain knowledge.

Relevant context can be retrieved from representative knowledge sources such as:

- Supply-chain data
- Risk scenarios
- Alternative routes

The retrieved information is supplied to the AI decision workflow before the final mitigation strategy is generated.

This allows the decision agent to reason using relevant system context rather than relying only on a generic LLM prompt.

---

## 📈 Machine Learning Risk Prediction

The prototype integrates an **XGBoost-based machine-learning component** into the risk workflow.

The model evaluates risk-related features such as:

- Risk score
- Severity
- Confidence
- Verification status

and produces an **intervention probability** indicating whether operational intervention may be required.

The ML layer works alongside AI reasoning rather than replacing it.

---

# 🌐 Energy Supply Chain Knowledge Graph

ETAI uses **Neo4j Aura** to model dependencies between supply-chain entities.

A simplified relationship structure is:

```text
Supplier
   │
   ▼
Origin Port
   │
   ▼
Shipping Route
   │
   ▼
Destination Port
   │
   ▼
Refinery
```

This graph-oriented representation provides a foundation for understanding how disruptions can propagate through interconnected supply-chain infrastructure.

The knowledge graph complements the relational database rather than replacing it.

---

# 🗺️ Geospatial Supply-Chain Representation

Ports and refineries contain geographic information represented through the project's geospatial database layer using:

- PostgreSQL
- PostGIS
- GeoAlchemy2

This provides a foundation for geographically aware infrastructure and route analysis.

---

# 🔬 Digital Twin & Scenario Simulation

ETAI contains a simulation layer for evaluating disruption scenarios.

Representative scenarios can model impacts such as:

- Supply loss
- Transportation delays
- Financial impact
- Infrastructure disruption
- Inventory pressure

Simulation information can be maintained through records such as:

- Simulation runs
- Simulation impacts
- Digital twin snapshots
- Simulation timelines

This allows the system to model how supply-chain conditions may change under disruption scenarios.

---

# 🛣️ Alternative Route Intelligence

When a transportation corridor becomes risky, ETAI can evaluate available mitigation alternatives.

The decision workflow can consider factors such as:

- Alternative ports
- Alternative shipping corridors
- Backup suppliers
- Additional transit time
- Route risk
- Estimated cost
- Available capacity
- Strategic reserve options

This information can then be used by the AI Decision Agent when generating mitigation recommendations.

---

# 💡 Recommendation & Decision System

ETAI maintains operational decision records rather than treating AI responses as temporary text.

The platform includes support for:

- Recommendations
- Decision actions
- Action outcomes

This creates the foundation for a decision lifecycle:

```text
Recommendation
      ↓
Decision
      ↓
Action
      ↓
Outcome
      ↓
Impact Evaluation
```

---

# 🛢️ Strategic Resilience

The platform architecture also supports resilience-related operational concepts including:

- Procurement
- Inventory
- Strategic reserves
- Alternative sourcing
- Supply diversification

These components allow disruption analysis to extend beyond transportation risk alone.

---

# 📰 Intelligence & Risk Events

Risk events are represented as structured operational intelligence.

The platform can maintain information such as:

- Event type
- Country or region
- Source
- Publication time
- Risk score
- Risk level
- AI confidence
- Explanation
- Verification status
- Event status

This structure provides a foundation for future continuous intelligence ingestion.

---

# 🛠️ Technology Stack

## Current Deployed Prototype

The following technologies are used in the current hackathon prototype:

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend/API | Python, FastAPI |
| ASGI Server | Uvicorn |
| API Communication | REST APIs, JSON |
| ORM | SQLAlchemy |
| Relational Database | PostgreSQL |
| Geospatial Layer | PostGIS, GeoAlchemy2 |
| Knowledge Graph | Neo4j Aura |
| Generative AI | Google Gemini |
| Agent Orchestration | LangGraph |
| AI Architecture | Retrieval-Augmented Generation (RAG) |
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Deployment | Render |
| Version Control | Git, GitHub |

---

# 🏗️ System Architecture

```text
                       ┌─────────────────────┐
                       │    ETAI Frontend    │
                       │  HTML / CSS / JS    │
                       └──────────┬──────────┘
                                  │
                              REST APIs
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │   FastAPI Backend   │
                       └──────────┬──────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      PostgreSQL/PostGIS      Neo4j Aura          AI / ML Layer
             │                    │                    │
             │              Knowledge Graph            │
             │                                         │
             └────────────────────┬────────────────────┘
                                  │
                                  ▼
                          Risk Intelligence
                                  │
                                  ▼
                         XGBoost Prediction
                                  │
                                  ▼
                       Digital Twin Simulation
                                  │
                                  ▼
                           RAG Retrieval
                                  │
                                  ▼
                       LangGraph Orchestrator
                                  │
                                  ▼
                           Gemini Agent
                                  │
                                  ▼
                    Mitigation Recommendation
                                  │
                                  ▼
                      Decision / Action / Outcome
```

---

# 🗄️ Hybrid Data Architecture

ETAI uses complementary relational and graph database models.

## PostgreSQL / PostGIS

The relational database manages operational and transactional information including entities and records such as:

- Suppliers
- Ports
- Refineries
- Shipping routes
- Risk events
- Risk score history
- Scenarios
- Simulation runs
- Simulation impacts
- Digital twin snapshots
- Recommendations
- Decision actions
- Action outcomes

PostGIS extends PostgreSQL with geospatial capabilities for geographically referenced infrastructure.

## Neo4j Aura

Neo4j represents relationships and dependencies across the supply-chain network.

The hybrid architecture separates two major responsibilities:

```text
PostgreSQL / PostGIS
        ↓
Operational, transactional and geospatial state

Neo4j
        ↓
Connected supply-chain relationships
```

---

# 📁 Project Structure

```text
ETAI-Hackathon/
│
├── ai_agents/             # AI agents and decision workflows
├── backend/               # FastAPI backend and API layer
├── data/                  # Supply-chain and scenario datasets
├── database/              # Database models/components
├── frontend/              # HTML/CSS/JavaScript dashboard
├── knowledge_graph/       # Neo4j knowledge graph integration
├── ml/                    # Machine-learning risk prediction
├── rag/                   # Retrieval-Augmented Generation pipeline
├── simulation/            # Digital twin and scenario simulation
├── tests/                 # Project tests
│
├── .gitignore
├── README.md
├── create_tables.py
├── requirements.txt
└── seed_database.py
```

---

# 🚀 Deployment Architecture

The prototype is deployed using Render.

```text
                    GitHub Repository
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      Render Static Site        Render Web Service
              │                         │
              ▼                         ▼
        ETAI Frontend             FastAPI Backend
                                        │
                                        ▼
                                PostgreSQL Database
```

The deployed frontend communicates with the deployed FastAPI backend through REST APIs.

---

# 🧪 Prototype Scope

ETAI is currently a **hackathon prototype and proof of concept**.

The goal of the prototype is to demonstrate that several technologies can be integrated into one coherent energy-resilience workflow:

```text
Risk
 ↓
Prediction
 ↓
Simulation
 ↓
Knowledge Retrieval
 ↓
AI Reasoning
 ↓
Recommendation
 ↓
Action
```

The prototype therefore prioritizes demonstrating the **complete end-to-end architecture and decision workflow** rather than operating at real-world national or enterprise scale.

The deployed application uses a controlled set of representative supply-chain entities, historical/representative intelligence, and disruption scenarios so that the complete workflow can be demonstrated reliably within hackathon infrastructure and time constraints.

---

# ⚠️ Prototype vs Production System

The current deployment is **not intended to be a production-ready system for making real-world critical energy infrastructure decisions**.

A production implementation would require substantially greater:

- Data coverage
- Real-time data ingestion
- Infrastructure capacity
- Security
- Reliability
- Model validation
- AI governance
- Monitoring
- Human oversight
- Enterprise integration

The current prototype instead demonstrates the **technical foundation and end-to-end decision architecture** on which a production system could be developed.

---

# 🚀 Production-Scale Vision

A production implementation would retain the core architectural concepts demonstrated by ETAI while replacing prototype-scale infrastructure with enterprise-grade systems.

## 🌍 Real-Time Intelligence Infrastructure

A production system could integrate continuously updated data sources such as:

- Maritime/AIS vessel intelligence
- Global geopolitical intelligence
- Weather and natural-disaster feeds
- Commodity market feeds
- Port and shipping information
- Government advisories
- Sanctions intelligence
- Refinery operational systems
- Inventory and procurement systems

Instead of relying primarily on representative prototype datasets, the production knowledge state would continuously evolve as new events arrive.

---

## ⚡ Event Streaming

At larger scale, an event-streaming platform such as **Apache Kafka or an equivalent technology** could be introduced.

This would allow intelligence events and operational updates to flow continuously through:

```text
External Data Sources
        ↓
Streaming Infrastructure
        ↓
Risk Processing
        ↓
Knowledge Graph Updates
        ↓
AI / ML Analysis
        ↓
Alerts & Decisions
```

> Event-streaming infrastructure is part of the proposed production architecture and is not claimed as part of the current hackathon deployment.

---

## 🧠 Production AI Infrastructure

The AI layer could evolve into a larger multi-agent architecture with specialized agents for areas such as:

- Risk intelligence
- Supplier analysis
- Route optimization
- Procurement
- Strategic reserves
- Simulation
- Decision evaluation

Production AI infrastructure would additionally require:

- Model evaluation pipelines
- AI observability
- Guardrails
- Human approval workflows
- Confidence thresholds
- Model fallback mechanisms
- Continuous knowledge updates
- Decision auditing

High-impact decisions could remain **human-controlled**, while AI continuously performs analysis and recommendation generation.

---

## 📚 Production RAG Infrastructure

The current RAG architecture could evolve into a continuously updated enterprise knowledge system incorporating:

- Operational documents
- Historical disruption records
- Government reports
- Market intelligence
- Supplier information
- Maritime intelligence
- Internal organizational knowledge

A dedicated production-scale vector database could be introduced to support substantially larger knowledge collections and retrieval workloads.

---

## 📈 Production Machine Learning

The ML layer could expand beyond prototype intervention prediction to models for:

- Time-series risk forecasting
- Supply disruption probability
- Supplier reliability prediction
- Route delay prediction
- Demand forecasting
- Inventory depletion forecasting
- Cost forecasting

Production ML infrastructure would also require:

- Model versioning
- Automated training pipelines
- Model monitoring
- Drift detection
- Evaluation datasets
- Feature management
- Retraining workflows

---

## 🌐 Large-Scale Knowledge Graph

The current Neo4j implementation demonstrates the concept of connected supply-chain dependency modeling.

A production graph could represent substantially larger networks connecting:

```text
Countries
    ↕
Suppliers
    ↕
Production Facilities
    ↕
Ports
    ↕
Tankers
    ↕
Shipping Routes
    ↕
Maritime Chokepoints
    ↕
Destination Ports
    ↕
Pipelines
    ↕
Refineries
    ↕
Storage Facilities
    ↕
Distribution Networks
```

This would enable disruption propagation analysis across a much broader energy ecosystem.

---

## 🔬 Advanced Digital Twin

A production digital twin could continuously synchronize with real operational data.

It could execute large numbers of simulations involving:

- Route closures
- Supplier outages
- Port failures
- Price shocks
- Demand surges
- Inventory shortages
- Sanctions
- Natural disasters
- Simultaneous multi-event disruptions

Alternative mitigation strategies could then be simulated and compared before recommendations reach operational decision-makers.

---

## ☁️ Enterprise Infrastructure

The current prototype uses a lightweight deployment suitable for demonstration.

A production implementation could introduce:

- Containerized backend services
- Horizontal scaling
- Background workers
- Distributed simulation workers
- Load balancing
- Caching
- High availability
- API gateways
- Centralized observability
- Fault tolerance
- Automated backups
- Disaster recovery

Technologies such as **Redis, container orchestration, managed cloud databases, and distributed processing infrastructure** could be introduced where appropriate.

These are **production-scale architectural directions and are not claimed as implemented in the current prototype**.

---

## 🔐 Production Security & Governance

A real-world critical infrastructure deployment would additionally require:

- Authentication
- Role-Based Access Control (RBAC)
- Encryption
- API authentication
- Secure secrets management
- Audit trails
- Network isolation
- Rate limiting
- Security monitoring
- Data governance
- AI decision auditing
- Human-in-the-loop approval

Different access levels could be provided to analysts, procurement teams, refinery operators, administrators, and government or enterprise decision-makers.

---

# 📊 Prototype → Production Evolution

| Current Hackathon Prototype | Production-Scale Direction |
|---|---|
| Representative supply-chain datasets | Continuous real-world data ingestion |
| Limited demonstration network | Large multi-country energy network |
| Prototype RAG knowledge | Continuously updated enterprise knowledge base |
| XGBoost intervention prediction | Multiple monitored forecasting models |
| Scenario-based digital twin | Continuously synchronized digital twin |
| Neo4j demonstration graph | Large dynamic/temporal knowledge graph |
| Render deployment | Enterprise cloud infrastructure |
| FastAPI application | Scalable containerized services |
| Demonstration workflows | Governed operational workflows |
| Prototype-scale processing | Distributed/high-availability processing |
| Basic prototype access | Authentication, RBAC and audit controls |

---

# 🌍 Potential Impact

A production-scale system based on this architecture could help organizations:

- Detect emerging supply-chain risks earlier
- Understand disruption propagation
- Compare alternative mitigation strategies
- Reduce supply interruption
- Improve supplier diversification
- Optimize strategic reserve decisions
- Reduce crisis response time
- Improve visibility across complex energy networks
- Support explainable, data-driven operational decisions

The objective is **not to replace human decision-makers**.

Instead, ETAI demonstrates how AI can transform fragmented supply-chain information into **structured, explainable decision intelligence**.

---

# 🔮 Future Scope

Potential future development includes:

- Real-time tanker tracking
- Live maritime intelligence
- Dynamic supplier discovery
- Multi-country supply-chain modeling
- Advanced disruption forecasting
- Automated procurement optimization
- Strategic reserve optimization
- Dynamic route optimization
- Large-scale digital twin simulations
- Temporal knowledge graphs
- Human-in-the-loop AI governance
- Enterprise authentication and authorization
- AI/model monitoring and observability

---

# ▶️ Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/prachi-01-ui/ETAI-Hackathon.git
cd ETAI-Hackathon
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a local `.env` file and configure the credentials required by the services used by the project.

Sensitive credentials must **never be committed to GitHub**.

These may include:

- Database connection information
- Gemini API credentials
- Neo4j credentials

## 5. Start the Backend

```bash
uvicorn backend.main:app --reload
```

The local backend will normally run at:

```text
http://127.0.0.1:8000
```

## 6. Start the Frontend

Serve the files inside the `frontend/` directory using a local development server.

The frontend communicates with the FastAPI backend through REST API requests.

---

# 🔒 Security Notice

Secrets and credentials are intentionally excluded from this repository.

Sensitive configuration should be supplied through environment variables rather than hardcoded into source files.

Do **not** commit:

- `.env` files
- API keys
- Database passwords
- Database connection URLs containing credentials
- Neo4j passwords
- Cloud-service credentials

---

# 🏁 Conclusion

ETAI demonstrates an end-to-end approach to **AI-powered energy supply-chain resilience**.

Rather than stopping at risk detection, the prototype connects:

**Risk Intelligence + Machine Learning + Knowledge Graphs + Digital Twin Simulation + RAG + Agentic AI + Decision Intelligence**

to demonstrate how future energy resilience systems could understand disruptions, evaluate their consequences, compare mitigation possibilities, and assist decision-makers in determining an appropriate response.

The current system is intentionally prototype-scale. Its modular architecture provides a foundation that could be expanded with real-time intelligence, enterprise infrastructure, significantly larger knowledge graphs, continuous digital twins, and production-grade AI governance.

---

# 🔗 Project Links

### 🌐 Live ETAI Platform

https://etai-energy-platform.onrender.com

### ⚙️ Backend API

https://etai-hackathon.onrender.com

### 💻 GitHub Repository

https://github.com/prachi-01-ui/ETAI-Hackathon

---

### ⚡ ETAI — From detecting disruption to deciding what to do next.
