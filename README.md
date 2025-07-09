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
