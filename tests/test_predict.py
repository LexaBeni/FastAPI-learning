import pytest
from sqlalchemy import select
from models.prediction import Prediction

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

def test_one_prediction(client, auth_headers, session, post_prediction):
    stmt = select(Prediction).order_by(Prediction.id.desc()).limit(1)
    prediction = session.scalars(stmt).first()
    res = client.get(f"/predict/history/{prediction.id}", headers=auth_headers)

    assert res.status_code == 200

def test_update_prediction(client, auth_headers, session, post_prediction):
    stmt = select(Prediction).order_by(Prediction.id)
    prediction = session.scalars(stmt).first()

    payload = {
        "title": "Updated title",
        "text": "Updated text",
        "note": "Updated note"
    }

    res = client.patch(f"/predict/update/{prediction.id}", json=payload, headers=auth_headers)

    assert res.status_code == 200

def test_delete_prediction(client, auth_headers, session, post_prediction):
    stmt = select(Prediction)

    prediction = session.execute(stmt)

    prediction = prediction.scalar_one_or_none()

    res = client.delete(f"/predict/delete/{prediction.id}", headers=auth_headers)

    assert res.status_code in (200, 204)

def test_invalid_delete(client, auth_headers, session, post_prediction):
    stmt = select(Prediction)

    prediction = session.execute(stmt)

    prediction = prediction.scalar_one_or_none()

    res = client.delete(f"/predict/delete/{999}", headers=auth_headers)
    
    assert res.status_code == 404








