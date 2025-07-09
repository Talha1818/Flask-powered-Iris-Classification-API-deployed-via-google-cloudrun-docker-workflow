from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)

# Load Iris dataset and train model
iris = load_iris()
X, y = iris.data, iris.target
model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Home route
@app.route('/', methods=['GET'])
def home():
    num_rows, num_cols = iris.data.shape
    feature_names = ', '.join(iris.feature_names)
    class_names = ', '.join(iris.target_names)

    return (
        f"Flask-powered Iris Classification API deployed via AWS ECS — Muhammad Talha\n\n"
        f"📊 Dataset Overview:\n"
        f"- Rows: {num_rows}\n"
        f"- Columns: {num_cols}\n"
        f"- Features: {feature_names}\n"
        f"- Target Classes: {class_names}\n"
    )


# Predict route
@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get values from URL query parameters
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))

        features = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)
        prediction = model.predict(features)
        class_name = iris.target_names[prediction[0]]

        return jsonify({
            'prediction': int(prediction[0]),
            'class_name': class_name
        })

    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid or missing query parameters.'}), 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
