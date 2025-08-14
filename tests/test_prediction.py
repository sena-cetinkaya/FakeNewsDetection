import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    payload = {"news": "sample news"}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert "result" in json_data
    assert json_data["result"] in ["gerçek", "sahte"]

