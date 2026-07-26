import pytest

def test_protected_endpoint_without_token(client):
    res = client.get("/predict/history")
    assert res.status_code == 401


def test_protected_endpoint_with_token(client, auth_headers):
    res = client.get("/predict/history", headers=auth_headers)
    assert res.status_code == 200

def test_predict_with_token(post_prediction):
    
    assert post_prediction.status_code == 200
    assert "prediction" in post_prediction.json()
    assert "probability" in post_prediction.json()

def test_predict_without_token(client):
    post = {
      "note": "Example request",
      "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars.",
      "title": "NASA launches new Mars rover"
    }

    res = client.post("/predict/", json=post)

    assert res.status_code == 401

