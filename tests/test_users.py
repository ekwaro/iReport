import pytest
import json
from application import app


class TestCases:
    @pytest.fixture()
    def client(self):
        test_client = app.test_client()
        return test_client

    def test_application_exists(self, client):
        response = client.get('/api/v1')
        assert response.status_code == 200
        assert b"You are welcome to iReport webpage" in response.data

    def test_register_user(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "di",
            "lastname": "dom",
            "othernames": "p",
            "email": "dom@hj.com",
            "phoneNumber": "234 345 7889",
            "username": "g",
            "password": "per5677hgg"
        }))
        assert response.status_code == 201

    def test_login_user(self, client):
        response = client.post('/api/v1/login', content_type="application/json", data = json.dumps(
            {
                "username": "dominic",
                "password": "123456789"
            }



        ))
        assert response.status_code == 200

    def test_login_wrong_user_name(self, client):
        response = client.post('/api/v1/login', content_type="application/json", data=json.dumps(
            {
                "username": "",
                "password": "123456789"
            }
        ))
        assert response.status_code == 400

    def test_login_wrong_password(self, client):
        response = client.post('/api/v1/login', content_type="application/json", data=json.dumps(
            {
                "username": "dominic",
                "password": ""
            }
        ))
        assert response.status_code == 400

    def test_wrong_firstname(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": 1,
            "lastname": "dom",
            "othernames": "p",
            "email": "dd@gmail.com",
            "phoneNumber": "234 666 8990",
            "username": "g",
            "password": "per5677hgg"
        }))
        assert response.status_code == 400

    def test_wrong_lastname(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "dom",
            "lastname": 4,
            "othernames": "p",
            "email": "dd@gmail.com",
            "phoneNumber": "234 456 8900",
            "username": "g",
            "password": "per5677hgg"
        }))
        respons = json.loads(response.data.decode())
        assert respons['status'] == 400
        assert respons['error'] == "lastname must be a word and must be filled in"

    def test_wrong_othernames(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "p",
            "lastname": "dom",
            "othernames": 4,
            "email": "dd@gmail.com",
            "phoneNumber": "235 666 890",
            "username": "g",
            "password": "per5677hgg"
        }))
        assert response.status_code == 400

    def test_wrong_email(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "p",
            "lastname": "dom",
            "othernames": "him",
            "email": 34,
            "phoneNumber": "245 678 8889",
            "username": "g",
            "password": "per5677hgg"
        }))
        assert response.status_code == 400

    def test_wrong_phonenumber(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "p",
            "lastname": "dom",
            "othernames": "him",
            "email": "pop@g.nn",
            "phoneNumber": "234 67 8076",
            "username": "doll",
            "password": "password"
        }))
        assert response.status_code == 400

    def test_wrong_username(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "p",
            "lastname": "dom",
            "othernames": "him",
            "email": "dd",
            "phoneNumber": "234 555 8900",
            "username": "",
            "password": "per5677hgg"
        }))
        assert response.status_code == 200

    def test_wrong_password(self, client):
        response = client.post('/api/v1/register', content_type="application/json", data=json.dumps({
            "firstname": "p",
            "lastname": "dom",
            "othernames": "him",
            "email": "pop@g.nn",
            "phoneNumber": "234 677 8076",
            "username": "doll",
            "password": "passwrd"
        }))
        assert response.status_code == 400

