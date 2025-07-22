# 🌸 Iris ML Prediction API — Flask + Google Cloud (GCP)

A lightweight Flask-based API for predicting Iris flower species using a pre-trained Logistic Regression model. This project utilizes the famous Iris dataset and is containerized for seamless deployment on Google Cloud Run using Docker and GitHub Actions**.

---

## 🚀 Overview

- **Language**: Python
- **Framework**: Flask
- **ML Library**: Scikit-learn
- **Dataset**: Iris (from `sklearn.datasets`)
- **Model**: Logistic Regression
- **Deployment**: Dockerized and ready for AWS ECS

---

## 📊 Dataset Info

- **Rows**: 150
- **Columns**: 4
- **Features**:
  - Sepal length (cm)
  - Sepal width (cm)
  - Petal length (cm)
  - Petal width (cm)
- **Target Classes**:
  - setosa
  - versicolor
  - virginica

---

## 🔌 API Endpoints

### `GET /`
Returns a welcome message and overview of the Iris dataset.

### `GET /predict`
Predicts the Iris flower class based on query parameters.

#### Example Request: (/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2)


#### Example Response:
```json
{
  "prediction": 0,
  "class_name": "setosa"
}

✅ Deployment Guide — Google Cloud Run + GitHub Actions
1. 📁 Project Structure
Ensure your repo contains:
app.py
requirements.txt
Dockerfile
.github/workflows/google-cloudrun-docker.yml

2. ✅ Enable Required GCP APIs
Go to Google Cloud Console and enable:

Cloud Run: run.googleapis.com

Artifact Registry: artifactregistry.googleapis.com

IAM Credentials API: iamcredentials.googleapis.com

3. 🏷️ Create Artifact Registry
Create a Docker repository in Artifact Registry. Example:

Region: us-central1
Name: iris-docker-repo
Format: Docker

4. 🔑 Create and Download GCP Service Account Key
Go to IAM & Admin > Service Accounts

Create a new account or select an existing one

Assign the following roles:

Artifact Registry Administrator

Cloud Run Admin

Click Create Key → JSON, then download it as gcp-key.json

5. 🔐 Add Secret to GitHub
Go to Repo Settings → Secrets and Variables → Actions

Add a new secret:

Name: GOOGLE_CREDENTIALS

Value: Paste contents of gcp-key.json

6. 🐳 Dockerfile Example
# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy contents
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app
CMD ["python", "app.py"]
7. 🧠 GitHub Actions Workflow
.github/workflows/google-cloudrun-docker.yml


name: 'Build and Deploy to Cloud Run'

on:
  push:
    branches:
      - master

env:
  PROJECT_ID: 'your-project-id'
  REGION: 'us-central1'
  SERVICE: 'iris-flask-api'
  REPO_NAME: 'iris-docker-repo'

jobs:
  deploy:
    runs-on: 'ubuntu-latest'

    permissions:
      contents: 'read'
      id-token: 'write'

    steps:
      - name: 'Checkout'
        uses: actions/checkout@v4

      - id: 'auth'
        name: 'Authenticate to Google Cloud'
        uses: google-github-actions/auth@v2
        with:
          credentials_json: '${{ secrets.GOOGLE_CREDENTIALS }}'

      - name: 'Configure Docker for GCP'
        run: |
          gcloud auth configure-docker "${{ env.REGION }}-docker.pkg.dev"

      - name: 'Build and Push Docker Image'
        run: |
          IMAGE="${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPO_NAME }}/${{ env.SERVICE }}:${{ github.sha }}"
          docker build -t "$IMAGE" .
          docker push "$IMAGE"

      - name: 'Deploy to Cloud Run'
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: '${{ env.SERVICE }}'
          region: '${{ env.REGION }}'
          image: '${{ env.REGION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPO_NAME }}/${{ env.SERVICE }}:${{ github.sha }}'

      - name: 'Show Service URL'
        run: echo ${{ steps.deploy.outputs.url }}

✨ Result
Once deployed, you’ll get a public URL (e.g., https://iris-flask-api-xxxx.a.run.app) where your ML model is hosted via Flask on Cloud Run, ready to receive real-time prediction requests.