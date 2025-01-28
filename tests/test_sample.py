from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sample_endpoint():
    response = client.get("/api/v1/sample")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}