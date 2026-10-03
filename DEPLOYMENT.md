# Deployment Guide: GCP Agentic Support Platform

This guide covers deploying the GCP Agentic Support Platform to Google Cloud Run using GitHub Actions CI/CD.

## Prerequisites

1. **Google Cloud Project**
   - Project ID: (e.g., `agentic-support-510416`)
   - GCP CLI installed and authenticated: `gcloud auth login`

2. **Service Account & Authentication**
   ```bash
   # Create a service account for Cloud Run deployment
   gcloud iam service-accounts create gcp-agentic-deploy \
     --display-name="GCP Agentic Deploy Service Account"
   
   # Grant necessary roles
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/artifactregistry.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"
   ```

3. **GitHub Secrets**
   Generate a key for the service account and add to GitHub Secrets:
   ```bash
   gcloud iam service-accounts keys create key.json \
     --iam-account=gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```
   
   Add to GitHub repository secrets:
   - `GCP_PROJECT_ID`: Your GCP project ID
   - `GCP_SA_KEY`: Contents of `key.json` (base64 encoded)

## Local Deployment (Manual)

### Step 1: Setup Environment
```bash
# Clone and setup
git clone https://github.com/bhargav-d-data-archive/gcp-agentic-support-platform.git
cd gcp-agentic-support-platform

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install google-adk
```

### Step 2: Configure GCP
```bash
# Set environment variables
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
export GOOGLE_CLOUD_LOCATION=us-central1

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Step 3: Deploy to Cloud Run
```bash
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --service_name=agentic-support-platform \
  --session_service_uri=memory:// \
  --env GOOGLE_GENAI_USE_VERTEXAI=TRUE \
  --env GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
  --env GOOGLE_CLOUD_LOCATION=us-central1 \
  support_agent \
  -- --no-allow-unauthenticated
```

### Step 4: Verify Deployment
```bash
# Get the service URL
gcloud run services describe agentic-support-platform --region=us-central1

# Test with authentication
gcloud run services call agentic-support-platform \
  --region=us-central1 \
  --data='{"message":"Hello from Cloud Run"}'
```

## Automated Deployment (GitHub Actions)

### Step 1: Add GitHub Secrets
Go to your GitHub repository Settings → Secrets and add:
- `GCP_PROJECT_ID`
- `GCP_SA_KEY`

### Step 2: GitHub Actions Workflow
The workflow file `.github/workflows/deploy.yml` automatically:
- Runs on every push to `main`
- Builds and pushes Docker image to Artifact Registry
- Deploys to Cloud Run
- Validates the deployment

### Step 3: Push and Deploy
```bash
git add .
git commit -m "Setup deployment"
git push origin main
```

Monitor deployment in GitHub Actions tab.

## Architecture on Cloud Run

```
Internet → Cloud Run (Private)
             ↓
          root_agent (Orchestrator)
             ↓
   ┌────────┼────────┐
   ↓        ↓        ↓
retrieval  reasoning action
  agent     agent    agent
   ↓                  ↓
 search_tool      ticket_tool
   ↓                  ↓
Vertex AI ←→ Gemini 2.5 Flash
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI instead of GenAI | `TRUE` |
| `GOOGLE_CLOUD_PROJECT` | GCP Project ID | `agentic-support-510416` |
| `GOOGLE_CLOUD_LOCATION` | GCP Region | `us-central1` |
| `CLOUD_RUN_SERVICE_NAME` | Cloud Run Service Name | `agentic-support-platform` |

## Troubleshooting

### Service won't start
```bash
# Check logs
gcloud run services logs read agentic-support-platform --region=us-central1 --limit 50

# Check build logs
gcloud builds log <BUILD_ID>
```

### Authentication errors
```bash
# Verify service account permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:gcp-agentic-deploy*"
```

### Vertex AI connection issues
```bash
# Verify Vertex AI API is enabled
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudrun.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

## Costs

- **Cloud Run**: ~$0.00001667 per vCPU-second + invocations
- **Vertex AI API**: Pay-per-use for Gemini requests
- **Artifact Registry**: $0.10 per GB stored (first 0.5GB free monthly)

## Rollback

```bash
# Rollback to previous revision
gcloud run services update-traffic agentic-support-platform \
  --to-revisions PREVIOUS_REVISION=100 \
  --region=us-central1
```

## Next Steps

1. Monitor logs in Cloud Logging
2. Set up Cloud Monitoring alerts
3. Enable Cloud Trace for distributed tracing
4. Configure API Gateway for external access
5. Set up Workload Identity for service authentication
