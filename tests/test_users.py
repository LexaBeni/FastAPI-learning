import pytest

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello world!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/auth/register", json={
        "email": "test@gmail.com",
        "username": "Test",
        "password": "test1"
    })
    assert res.status_code == 201
    assert res.json()["email"] == "test@gmail.com"



def test_login(client, test_user):
    res = client.post("/auth/login", data={
            "username": test_user['username'],
            "password": test_user['password']})
    assert res.status_code == 200

def test_login_success(login_user):
    assert "access_token" in login_user
    assert "refresh_token" in login_user
    assert login_user['token_type'] == "bearer"


def test_create_user_duplicate(client):
    user_data = {
        "email": "test@gmail.com",
        "username": "Test",
        "password": "test1"
    }

    first = client.post("/auth/register", json=user_data)
    assert first.status_code == 201

    second = client.post("/auth/register", json=user_data)
    assert second.status_code in (400, 409)

@pytest.mark.parametrize("password", ["wrong", "123", " "])
def test_login_incorrect_password(client, test_user, password):
    res = client.post("/auth/login", data={"username": test_user['username'], "password": password})

    assert res.status_code == 401

def test_refresh_token(client, login_user):
    res = client.post("/auth/refresh", json={"refresh_token": login_user['refresh_token']})

    assert res.status_code == 200

    assert "access_token" in res.json()