# Quick Start: Deploy in 5 Minutes

## Option 1: Automatic Deployment (GitHub Actions)

### 1. Add GitHub Secrets
Go to **Settings → Secrets and variables → Actions**

Add these secrets:
- `GCP_PROJECT_ID`: Your GCP project ID (e.g., `agentic-support-510416`)
- `GCP_SA_KEY`: Service account JSON key (base64 encoded)

To create the service account:
```bash
# Run these commands locally
gcloud iam service-accounts create gcp-agentic-deploy \
  --display-name="GCP Agentic Deploy"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"

gcloud iam service-accounts keys create key.json \
  --iam-account=gcp-agentic-deploy@YOUR_PROJECT_ID.iam.gserviceaccount.com

cat key.json | base64
```

### 2. Push to Main
```bash
git add .
git commit -m "Setup Cloud Run deployment"
git push origin main
```

### 3. Watch the Deployment
- Go to **Actions** tab in GitHub
- Click the latest workflow run
- Watch it deploy automatically

---

## Option 2: Manual Deployment (gcloud CLI)

### 1. Setup (one-time)
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 2. Deploy
```bash
# From the repository root
adk deploy cloud_run \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --service_name=agentic-support-platform \
  --env GOOGLE_GENAI_USE_VERTEXAI=TRUE \
  --env GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
  --env GOOGLE_CLOUD_LOCATION=us-central1 \
  support_agent \
  -- --no-allow-unauthenticated
```

### 3. Test
```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe agentic-support-platform \
  --region=us-central1 \
  --format='value(status.url)')

echo "Service running at: $SERVICE_URL"

# Make an authenticated request
gcloud run services call agentic-support-platform \
  --region=us-central1 \
  --data='{"message":"Hello"}'
```

---

## Verify Deployment

```bash
# Check service status
gcloud run services describe agentic-support-platform --region=us-central1

# View recent logs
gcloud run services logs read agentic-support-platform --region=us-central1 --limit=20

# Monitor traffic
gcloud monitoring dashboards create --config-from-file=/dev/stdin <<EOF
{
  "displayName": "Agentic Support Platform",
  "mosaicLayout": {
    "columns": 12,
    "tiles": [
      {
        "width": 6,
        "height": 4,
        "widget": {
          "title": "Cloud Run Requests",
          "xyChart": {
            "dataSets": [{
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "resource.type=\"cloud_run_revision\" resource.labels.service_name=\"agentic-support-platform\""
                }
              }
            }]
          }
        }
      }
    ]
  }
}
EOF
```

---

## Next Steps

✅ **Service is deployed!**

- Read the full [DEPLOYMENT.md](./DEPLOYMENT.md) guide
- Check logs: `gcloud run services logs read agentic-support-platform --region=us-central1`
- Set up API Gateway for external access
- Configure monitoring and alerts
- Review [README.md](./README.md) for architecture details

---

## Troubleshooting

**Service won't start:**
```bash
gcloud run services logs read agentic-support-platform --region=us-central1 --limit=50
```

**Permission denied:**
```bash
gcloud projects get-iam-policy YOUR_PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:gcp-agentic-deploy*"
```

**Still stuck?**
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting
- Review [Full README](./README.md)
