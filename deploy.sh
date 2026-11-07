#!/usr/bin/env bash
# ==============================================================================
# World Pulse Chronicle - Cloud Run & Cloud Scheduler Deployment Script
# Architecture: GCP Always Free Tier (Cloud Run 512MiB/1CPU + Firestore + Scheduler)
# ==============================================================================
set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value core/project --quiet)}"
REGION="${GCP_REGION:-us-central1}"
SCHEDULER_LOCATION="${GCP_SCHEDULER_LOCATION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-world-pulse-chronicle}"
SCHEDULER_JOB_NAME="${SCHEDULER_JOB_NAME:-world-pulse-weekly-sync}"
GEMINI_MODEL="${GEMINI_MODEL:-gemini-3.8-flash}"

if [[ -z "${PROJECT_ID}" ]]; then
  echo "Error: GCP_PROJECT_ID is not set and no active gcloud project was found." >&2
  exit 1
fi

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "Error: GEMINI_API_KEY environment variable is required." >&2
  exit 1
fi

if [[ -z "${UPDATE_SECRET_TOKEN:-}" ]]; then
  echo "Error: UPDATE_SECRET_TOKEN environment variable is required." >&2
  exit 1
fi

echo "==> [Step 1] Validating leaf-level gcloud CLI syntax..."
gcloud help run deploy --quiet >/dev/null
gcloud help run services describe --quiet >/dev/null
gcloud help scheduler jobs describe --quiet >/dev/null
gcloud help scheduler jobs create http --quiet >/dev/null
gcloud help scheduler jobs update http --quiet >/dev/null

# Prepare root Dockerfile from backend/Dockerfile for Cloud Build source deploy
cp -f backend/Dockerfile ./Dockerfile
cleanup() {
  rm -f ./Dockerfile
}
trap cleanup EXIT

echo "==> [Step 2] Deploying Cloud Run service '${SERVICE_NAME}' in ${REGION} (Always Free limits)..."
gcloud run deploy "${SERVICE_NAME}" \
  --source=. \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=1 \
  --timeout=300 \
  --set-env-vars="GEMINI_API_KEY=${GEMINI_API_KEY},UPDATE_SECRET_TOKEN=${UPDATE_SECRET_TOKEN},GEMINI_MODEL=${GEMINI_MODEL},GCP_PROJECT_ID=${PROJECT_ID}" \
  --quiet

echo "==> [Step 3] Resolving deployed Cloud Run URL..."
SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format="value(status.url)" \
  --quiet)"

if [[ -z "${SERVICE_URL}" ]]; then
  echo "Error: Failed to retrieve Cloud Run service URL." >&2
  exit 1
fi

echo "    Service URL: ${SERVICE_URL}"

echo "==> [Step 4] Configuring Cloud Scheduler job '${SCHEDULER_JOB_NAME}' (Every Day 06:00 JST - 1 Run/Day)..."
if gcloud scheduler jobs describe "${SCHEDULER_JOB_NAME}" \
  --project="${PROJECT_ID}" \
  --location="${SCHEDULER_LOCATION}" \
  --format="json(name)" \
  --quiet >/dev/null 2>&1; then
  gcloud scheduler jobs update http "${SCHEDULER_JOB_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${SCHEDULER_LOCATION}" \
    --schedule="0 6 * * *" \
    --time-zone="Asia/Tokyo" \
    --uri="${SERVICE_URL}/api/update" \
    --http-method=POST \
    --update-headers="X-Update-Token=${UPDATE_SECRET_TOKEN},Content-Type=application/json" \
    --attempt-deadline=300s \
    --quiet
else
  gcloud scheduler jobs create http "${SCHEDULER_JOB_NAME}" \
    --project="${PROJECT_ID}" \
    --location="${SCHEDULER_LOCATION}" \
    --schedule="0 6 * * *" \
    --time-zone="Asia/Tokyo" \
    --uri="${SERVICE_URL}/api/update" \
    --http-method=POST \
    --headers="X-Update-Token=${UPDATE_SECRET_TOKEN},Content-Type=application/json" \
    --attempt-deadline=300s \
    --quiet
fi

echo "==> Deployment complete!"
echo "    Web UI : ${SERVICE_URL}/"
echo "    API    : ${SERVICE_URL}/api/latest"
echo "    Update : POST ${SERVICE_URL}/api/update (Header: X-Update-Token)"
