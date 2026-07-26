import pytest

def test_protected_endpoint_without_token(client):
    res = client.get("/predict/history")
    assert res.status_code == 401


def test_protected_endpoint_with_token(client, auth_headers):
    res = client.get("/predict/history", headers=auth_headers)
    assert res.status_code == 200

@pytest.mark.parametrize("payload", [
    {
        "note": "Example request",
        "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars.",
        "title": "NASA launches new Mars rover"
    },
    {
        "note": "Another example",
        "text": "Scientists discovered water on a distant planet.",
        "title": "New discovery"
    }
])
def test_predict_with_token(client, auth_headers, payload):
    res = client.post("/predict/", json=payload, headers=auth_headers)
    assert res.status_code == 200
    assert "prediction" in res.json()
    assert "probability" in res.json()

def test_predict_without_token(client):
    post = {
      "note": "Example request",
      "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars.",
      "title": "NASA launches new Mars rover"
    }

    res = client.post("/predict/", json=post)

    assert res.status_code == 401

def test_predict_without_label(client, auth_headers):
    post = {
          "note": "Example request",
          "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars."
        }
    res = client.post("/predict/", json=post, headers=auth_headers)

    assert res.status_code == 422


