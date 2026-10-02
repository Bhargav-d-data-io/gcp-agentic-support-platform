# GCP Agentic Customer Support Platform

A cloud-deployed multi-agent customer support application built with **Google Agent Development Kit (ADK)**, **Gemini 2.5 Flash on Vertex AI**, **Python**, **Google Cloud Run**, and **Vertex AI Agent Engine**.

The platform uses a root customer-support orchestrator to route requests to specialized retrieval, reasoning, and action agents. The current implementation supports knowledge retrieval, support-ticket creation, ADK session handling, correlation IDs for support operations, and authenticated deployment on Google Cloud Run.

## Architecture

```text
Client / API Request
        |
        v
Google Cloud Run
        |
        v
Customer Support Orchestrator
        |
        +----------------+----------------+
        |                |                |
        v                v                v
 Retrieval Agent   Reasoning Agent   Action Agent
        |                                 |
        v                                 v
 Knowledge Tool                       Ticket Tool
        |                                 |
        +---------------+-----------------+
                        |
                        v
                Gemini 2.5 Flash
                   Vertex AI
```

## Multi-Agent Design

The application is organized around a Google ADK root orchestrator with three specialized agents:

- **Retrieval Agent** — handles customer-support knowledge requests and invokes the support knowledge tool.
- **Reasoning Agent** — provides a dedicated agent path for reasoning-oriented support tasks.
- **Action Agent** — performs support actions such as creating escalation tickets.
- **Customer Support Orchestrator** — analyzes incoming requests and transfers control to the appropriate specialized agent.

## Implemented Features

- Multi-agent orchestration using **Google ADK**
- **Gemini 2.5 Flash** through Vertex AI
- Retrieval, reasoning, and action agent architecture
- ADK agent-to-agent transfer and tool calling
- Support knowledge retrieval tool
- Support-ticket creation tool
- ADK invocation-based correlation IDs propagated across orchestrator, specialized agents, and tool results
- ADK session-service integration and multi-turn session demo
- Containerized deployment through the ADK Cloud Run workflow
- Private authenticated **Google Cloud Run** service
- Container build and storage through **Cloud Build** and **Artifact Registry**
- Deployed ADK API endpoints for session creation and agent execution
- **Vertex AI Agent Engine** managed deployment
- Managed Agent Engine session continuity
- **Memory Bank** persistence using an ADK after-agent callback
- **PreloadMemoryTool** integration for long-term memory retrieval
- Verified cross-session recall of stored user preferences
- Git and GitHub source control

## Verified Cloud Deployment

The application has been deployed to **Google Cloud Run** in `us-central1`.

A deployed API test verified this execution path:

```text
API Request
   |
   v
Cloud Run
   |
   v
Customer Support Orchestrator
   |
   v
Retrieval Agent
   |
   v
search_support_knowledge()
   |
   v
Gemini 2.5 Flash
   |
   v
Grounded Support Response
```

A separate action-agent test verified support-ticket creation with a generated **ticket ID** and **correlation ID**.

The Cloud Run service is configured for authenticated access rather than unrestricted public invocation.

## Technology Stack

| Layer | Technology |
|---|---|
| Agent Framework | Google Agent Development Kit (ADK) 2.11 |
| LLM | Gemini 2.5 Flash |
| AI Platform | Vertex AI |
| Language | Python |
| Compute | Google Cloud Run + Vertex AI Agent Engine |
| Container Build | Cloud Build |
| Container Registry | Artifact Registry |
| Session Layer | ADK In-Memory Sessions + Managed Agent Engine Sessions |
| Long-Term Memory | Vertex AI Memory Bank + ADK PreloadMemoryTool |
| Source Control | Git + GitHub |

## Local Setup

Clone the repository:

```bash
git clone https://github.com/Bhargav-d-data-io/gcp-agentic-support-platform.git
cd gcp-agentic-support-platform
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install Google ADK:

```bash
pip install google-adk
```

Configure Vertex AI:

```bash
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
export GOOGLE_CLOUD_LOCATION=us-central1
```

Authenticate with Google Cloud and ensure the required Google Cloud APIs are enabled.

Run the agent locally:

```bash
adk run support_agent
```

## Cloud Run Deployment

The application can be deployed using the Google ADK Cloud Run deployment workflow:

```bash
adk deploy cloud_run \
  --project=YOUR_GCP_PROJECT_ID \
  --region=us-central1 \
  --service_name=agentic-support-platform \
  --session_service_uri=memory:// \
  --env GOOGLE_GENAI_USE_VERTEXAI=TRUE \
  --env GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID \
  --env GOOGLE_CLOUD_LOCATION=us-central1 \
  support_agent \
  -- --no-allow-unauthenticated
```

The current deployment uses **authenticated Cloud Run access** and an **in-memory ADK session service**.

## Project Structure

```text
gcp-agentic-support-platform/
├── support_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── session_demo.py
├── .gitignore
└── README.md
```

## Current Project Status

### Implemented and Tested

- Google ADK multi-agent architecture
- Root orchestrator with retrieval, reasoning, and action agents
- Retrieval-agent routing and knowledge-tool execution
- Action-agent routing and support-ticket creation
- Gemini 2.5 Flash integration through Vertex AI
- ADK invocation-based correlation IDs propagated across orchestrator, specialized agents, and tool results
- Cloud Run deployment
- Authenticated Cloud Run access
- Deployed ADK API execution
- Vertex AI Agent Engine managed deployment
- Managed Agent Engine session continuity
- Memory Bank persistence through ADK callback integration
- PreloadMemoryTool-based long-term memory retrieval
- Cross-session recall of stored user preferences

### Planned Enhancements

The following capabilities are planned and are **not represented as completed features**:

- Embedding-based vector retrieval
- Tenant-aware persistent memory
- Cloud Trace / OpenTelemetry integration
- API Gateway and external ingress
- Workload Identity and service-to-service authorization
- Secret Manager integration
- Terraform-based infrastructure
- Automated CI/CD with GitHub Actions or Cloud Build

## Purpose

This project demonstrates the design and deployment of an agentic AI application on Google Cloud, with emphasis on **multi-agent orchestration, tool execution, cloud deployment, session handling, security boundaries, and production-oriented architecture**.
