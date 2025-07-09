# 🌸 Iris ML Prediction API — Flask + AWS ECS

A lightweight Flask-based API for predicting Iris flower species using a pre-trained Logistic Regression model. The project uses the famous Iris dataset and is containerized for deployment on **AWS Elastic Container Service (ECS)**.

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

## ✅ CI/CD with GitHub Actions

```yaml
name: Flask Test CI

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v3

    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest

    - name: 🧪 Run unit tests
      run: PYTHONPATH=. pytest tests/

### "enableFaultInjection" is not part of standard ECS task definitions.

## ✅ CI/CD with GitHub Actions - Login in ECS

```yaml
name: "CI/CD - Flask Test, Build & Deploy to ECS"

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

env:
  AWS_REGION: us-west-1
  ECR_REPOSITORY: talha-ecr-repositry
  ECS_SERVICE: muhammad-talha-task-service-2fccmkqn 
  ECS_CLUSTER: talha-cluster
  ECS_TASK_DEFINITION: .aws/taskdef.json
  CONTAINER_NAME: muhammad-talha-container

permissions:
  contents: read

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest

    - name: 🧪 Run tests
      run: |
        PYTHONPATH=. pytest tests/

    - name: 🔐 Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: 🔐 Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: 🐳 Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

    - name: 🧩 Render ECS task definition with new image
      id: task-def
      uses: aws-actions/amazon-ecs-render-task-definition@v1
      with:
        task-definition: ${{ env.ECS_TASK_DEFINITION }}
        container-name: ${{ env.CONTAINER_NAME }}
        image: ${{ steps.build-image.outputs.image }}

    - name: 🚀 Deploy to ECS
      uses: aws-actions/amazon-ecs-deploy-task-definition@v1
      with:
        task-definition: ${{ steps.task-def.outputs.task-definition }}
        service: ${{ env.ECS_SERVICE }}
        cluster: ${{ env.ECS_CLUSTER }}
        wait-for-service-stability: true

