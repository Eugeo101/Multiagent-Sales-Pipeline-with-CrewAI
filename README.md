# Sales-Pipeline-Flow — CrewAI Multi-Agent Lead Qualification Network

This repository implements a production-grade automated sales pipeline using **CrewAI Flows**. It orchestrates two distinct specialized agentic **Crews** (`LeadScoringCrew` and `EmailWritingCrew`) to ingest raw lead form data, perform rigorous background profile validation and cultural fit analysis, and generate highly targeted, conversion-optimized outbound follow-up drafts using **Google Gemini** infrastructure.

---

## Project Structure

```text
sales_pipeline_flow/
├── pyproject.toml              ← App dependencies, metadata, and Python constraints (>=3.11)
├── uv.lock                     ← Deterministic dependency lockfile
├── .env                        ← Local credentials & API keys (do not commit)
├── .gitignore                  ← Prevents leaking credentials or virtual environments
│
└── src/
    └── sales_pipeline_flow/
        ├── __init__.py
        ├── main.py             ← Event-driven Flow router orchestration (@flow, @start, @listen)
        │
        └── crews/
            ├── lead_scoring_crew/
            │   ├── lead_scoring_crew.py  ← Crew builder, Pydantic data schema enforcement
            │   └── config/
            │       ├── agents.yaml       ← Roles, goals, backstories for verification specialists
            │       └── tasks.yaml        ← Context parsing and numerical indexing configurations
            │
            └── email_writing_crew/
                ├── email_writing_crew.py ← Crew class mappings and LLM hook connections
                └── config/
                    ├── agents.yaml       ← Content specialists & engagement strategists configs
                    └── tasks.yaml        ← Personalization parameters and CTA injection logic

```

---

## Setup

Ensure you are working in an environment running **Python 3.11, 3.12, or 3.13** to satisfy core vector tracking wheel allocations (`onnxruntime`).

### 1. Initialize Environment & Sync Dependencies

```bash
# Sync environment dependencies using uv (highly recommended)
uv sync

# Or alternatively install using standard packages
pip install -r requirements.txt

```

### 2. Configure Local Authentication

Create a `.env` file in the root folder of your project workspace:

```bash
GOOGLE_API_KEY="YourGeminiKeyHere"

```

---

## Configuration Mappings

### Agent Setup (`config/agents.yaml`)

Your infrastructure runs on 5 highly decoupled agent profiles split across two separate operational pools:

| Crew Pool | Agent Name | Primary Operational Responsibility |
| --- | --- | --- |
| **Lead Scoring** | `lead_data_agent` | Extracts and profiles structured metadata from raw input text logs. |
| **Lead Scoring** | `cultural_fit_agent` | Benchmarks lead goals against CrewAI enterprise deployment pitches. |
| **Lead Scoring** | `scoring_validation_agent` | Aggregates matrix profiles into a validated structural Pydantic report. |
| **Email Writing** | `email_content_specialist` | Generates short, point-to-point contextual personalized draft copy. |
| **Email Writing** | `engagement_strategist` | Strips out generic salutations; forces immediate conversion hooks & CTAs. |

---

## Usage Examples

### 1. Local Pipeline Execution

To execute your event-driven flow locally through the command-line interface executor:

```bash
python -m crewai run

```

When kicked off, the pipeline receives input context via the flow runner wrapper layer:

```python
inputs = {
    "name": "Jane Doe",
    "job_title": "Director of AI Infrastructure",
    "company": "Enterprise Corp",
    "email": "jane@enterprisecorp.com",
    "use_case": "Looking to orchestrate hundreds of autonomous workers across legacy databases."
}

```

### 2. Cloud Production Deployment (CrewAI AMP)

To host your autonomous pipeline agents as managed, low-latency microservices on the Agent Management Platform:

```bash
# Step 1: Connect your local terminal instance to the platform dashboard
python -m crewai.cli.cli login

# Step 2: Bind workspace references to your remote private GitHub repository container
python -m crewai.cli.cli deploy create --skip-validate

# Step 3: Compile, push your branches live, and instantiate production web endpoints
python -m crewai deploy push

```

---

## Operational Pipeline Mechanics

```text
[Raw Input Parameters] 
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ 1. LEAD SCORING CREW                                   │
│    - Profile Harvesting ────> Cultural Alignment Matrix│
│    - Score Index (0-100)                               │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼ (Pydantic Output Model Bridge)
┌────────────────────────────────────────────────────────┐
│ 2. EMAIL WRITING CREW                                  │
│    - Personalized Drafting ──> Conversion Optimization │
│    - Removal of Fluff & Closing Salutations            │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
[Optimized Outbound Discovery Email Output Ready to Send]

```

| Pipeline Task Step | Handled By | Input Requirements | Generated Artifact Result |
| --- | --- | --- | --- |
| `lead_data_collection` | `lead_data_agent` | `{name}`, `{company}`, `{use_case}` | Comprehensive Personal & Corporate Data Report |
| `cultural_fit_analysis` | `cultural_fit_agent` | Captured Dossier Data | Strategic alignment assessment & index (0 to 10) |
| `lead_scoring_and_validation` | `scoring_validation_agent` | Aggregated Analytics | Clean Pydantic Payload (`score`, `personal_info`, `company_info`) |
| `email_drafting` | `email_content_specialist` | Parsed Pydantic Payload | Raw, highly targeted personalized inline response text |
| `engagement_optimization` | `engagement_strategist` | Raw Content Draft | Finalized outbound email draft containing high-impact CTAs |

---

## Implementation Notes

* **Security Guardrails**: The project root uses strict `.gitignore` patterns. Under no circumstances should your local `.env` key registers be tracked or pushed to public remote repositories.
* **Windows Environment Management**: If you encounter an `Access is denied (os error 5)` bug during deployment compilation runs on Windows platforms, bypass local validation checks using the `--skip-validate` configuration switch; the remote cloud infrastructure environment operates securely on independent native Linux system setups.
* **Data Flow Safety**: Data between independent crews moves safely by forcing structural schema conversions using Pydantic models attached right to the validation task definitions before mapping properties into downstream execution queues.