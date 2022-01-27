from fastapi.testclient import TestClient
from api.app import app
from http import HTTPStatus

USER = {
  "username": "test12345",
  "password": "test12345"
}

WRONG_BODY = {
  "username": "no",
  "password": "no"
}

client = TestClient(app)


def test_no_connection_without_token():
    response = client.get('/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get('/monster')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get('/monster/test')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get('/users/me')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get('/users/me/items')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_register():
    response = client.post('/register')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response = client.post('/register', json=USER)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"Info": "Successful registrations! Go to /token to get a token"}


def test_token_take_registered_user():
    client.post('/register', json=USER)
    response = client.post('/token', json=USER)
    assert response.status_code == HTTPStatus.OK


def test_token_take_not_registered_user():
    response = client.post('/token')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response = client.post('/token', json=WRONG_BODY)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}


def test_connection_with_token():
    client.post('/register', json=USER)
    client.post('/token', json=USER)
    test_token = client.post('/token', json=USER).json()['access_token']
    test_token_value = 'Bearer Token ' + test_token

    response = client.get('/', headers={"Authorization": test_token_value})
    assert response.status_code == HTTPStatus.OK

    response = client.get('/monster', headers={"Authorization": test_token_value})
    assert response.status_code == HTTPStatus.OK

    response = client.get('/monster/test', headers={"Authorization": test_token_value})
    assert response.status_code == HTTPStatus.OK
