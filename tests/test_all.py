from fastapi.testclient import TestClient
from api.app import app, cache
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
    response = client.get('/monster/test')
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = client.get('/users/me')
    assert response.status_code == HTTPStatus.UNAUTHORIZED


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

    response = client.get('/monster/test', headers={"Authorization": test_token_value})
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'image/png'


def test_cache():
    cache.flushdb()
    client.post('/register', json=USER)
    client.post('/token', json=USER)
    test_token = client.post('/token', json=USER).json()['access_token']
    test_token_value = 'Bearer Token ' + test_token

    assert cache.get('test_cache') is None
    client.get('/monster/test_cache', headers={"Authorization": test_token_value})
    assert cache.get('test_cache') is not None
