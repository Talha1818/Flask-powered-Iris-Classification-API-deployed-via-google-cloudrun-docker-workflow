from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

    response_text = response.data.decode('utf-8')

    assert "Muhammad Talha" in response_text
    assert "Rows: 150" in response_text
    assert "Columns: 4" in response_text
    assert "setosa" in response_text  # One of the class names
    assert "sepal length" in response_text  # One of the features
