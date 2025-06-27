import pytest
from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Test case for the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Custom Chat Bot API!"}
