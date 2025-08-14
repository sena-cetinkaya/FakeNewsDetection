import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    payload = {"news": "los angeles polis teşkilatı ’ arşivine ulaşan polis mike rothmiller kitabında marilyn monroe ’ ölümünü anlattı rothmiller hollywood ’ efsanevi yıldızının abd başkanı john kennedy ’ erkek kardeşi robert kennedy öldürüldüğü iddia etti polis memuru mike rothmiller los angeles polis arşivinde yaptığı araştırmada ’ efsane oyuncusu marilyn monroe ’ dönemin abd başkanı john kennedy ’ erkek kardeşi robert kennedy öldürüldüğüne bilgilere ulaştığını iddia etti"}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    json_data = response.json()
    assert "result" in json_data
    assert json_data["result"] in ["gerçek", "sahte"]
