@echo off
REM Build Docker image for file-upload
docker build -t ekg-cre-metrics .

REM Tag Docker image for Google Cloud registry
docker tag ekg-cre-metrics YOUR_GCP_REGION-docker.pkg.dev/YOUR_GCP_PROJECT_ID/YOUR_REPO/trade-recommendation
REM Push Docker image to Google Cloud registry
docker push YOUR_GCP_REGION-docker.pkg.dev/YOUR_GCP_PROJECT_ID/YOUR_REPO/trade-recommendation
echo 
pause
