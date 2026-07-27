from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import settings
from dependencies.database import get_db
from core.database import Base
from fastapi.testclient import TestClient
import pytest
from main import app
import numpy as np


test_engine = create_engine(settings.test_database_url)

TestingSessionLocal = sessionmaker(test_engine, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

class DummyModel:
    def predict(self, X):
        return np.array([1])   

    def predict_proba(self, X):
        return np.array([[0.1, 0.9]])

@pytest.fixture(scope="function")
def client():

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db
    app.state.model = DummyModel()

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    data ={
        "email": "test@gmail.com",
        "username": "Test",
        "password": "test1"}

    res = client.post("/auth/register", json = data)

    new_user = res.json()
    new_user['password'] = data["password"]
    return new_user

@pytest.fixture
def login_user(client, test_user):
    res = client.post("/auth/login", data={"username": test_user['username'], "password": test_user["password"]})
    assert res.status_code == 200
    return res.json()

@pytest.fixture
def access_token(login_user):
    return login_user['access_token']

@pytest.fixture
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def post_prediction(client, auth_headers):
    post = {
  "note": "Example request",
  "text": "NASA successfully launched a new rover to explore ancient riverbeds on Mars.",
  "title": "NASA launches new Mars rover"
}
    res = client.post("/predict/", json=post, headers=auth_headers)

    return res



