import pytest
import json
from application import app


class TestIncidents:
    @pytest.fixture()
    def client(self):
        test_client = app.test_client()
        return test_client

    @pytest.fixture()
    def login_user(self, client):
        """

        """
        response = client.post('/api/v1/login', content_type='application/json', data=json.dumps(dict(
            username="dominic",
            password="123456789"
        )))
        data = json.loads(response.data.decode())
        item = data['data'][0]
        return item

    @pytest.fixture()
    def post_content(self, client, login_user):
        token = login_user
        response = client.post('api/v1/redflags', headers=dict(Authorization='Bearer ' + token),
                               content_type='application/json', data=json.dumps(dict(
                incident_type="red-flag",
                status="draft",
                comment="comments",
                location=0.11
            )))
        return response

    def test_post_incident(self, post_content):

        data = json.loads(post_content.data.decode())
        assert data['status'] == 201

    def test_input_wrong_incident_type(self, client, login_user):
        token = login_user
        response = client.post('api/v1/redflags', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
            incident_type="redflag",
            status="draft",
            comment="comments",
            location=0.111
        )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['message'] == "Incident_type must be either a red flag or Intervention record "

    def test_input_wrong_status(self, client, login_user):
        token = login_user
        response = client.post('api/v1/redflags', headers=dict(Authorization='Bearer ' + token),content_type='application/json', data=json.dumps(dict(
                incident_type="red-flag",
                status="draft is",
                comment="comments",
                location=0.111
            )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['message'] == "status must be either (draft, resolved, rejected,under investigation)"

    def test_input_wrong_comment(self, client, login_user):
        token = login_user
        response = client.post('api/v1/redflags', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
                incident_type="red-flag",
                status="draft",
                comment=5,
                location=0.111
            )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['message'] == "Comment must be a sentence"

    def test_input_wrong_location(self, client, login_user):
        token = login_user
        response = client.post('api/v1/redflags', headers=dict(Authorization='Bearer ' + token),content_type='application/json', data=json.dumps(dict(
                incident_type="red-flag",
                status="draft",
                comment="",
                location=111
            )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['message'] == "location must be filled and must be a number of the form 1.0000"

    def test_get_all_items_failure(self, client, login_user):
        token = login_user
        response = client.get('/api/v1/redflags', headers=dict(Authorization='Bearer ' + token))
        data = json.loads(response.data.decode())
        assert data['status'] == 200

    def test_failure_get_specific_item(self, client, login_user):
        token = login_user
        response = client.get('/api/v1/redflags/9', headers=dict(Authorization='Bearer ' + token))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['error'] == "Item with the Id not found"

    def test_success_get_single_item(self, client, login_user):
        token = login_user
        response = client.get('/api/v1/redflags/1', headers=dict(Authorization='Bearer ' + token))
        data = json.loads(response.data.decode())
        assert data['status'] == 200

    def test_success_updating_comment(self, client, login_user):
        token = login_user
        response = client.patch('/api/v1/redflags/1/comment', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
           comment="This is a new comment"
        )))
        data = json.loads(response.data.decode())
        assert data['status'] == 200
        assert data['message'] == "Updated red-flag record’s comment"

    def test_failure_updating_comment(self, client, login_user):
        token = login_user
        response = client.patch('/api/v1/redflags/1/comment', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
            comment=5

        )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400

    def test_failure_updating_location(self, client, login_user):
        token = login_user
        response = client.patch('/api/v1/1/location', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
            location=''

        )))
        data = json.loads(response.data.decode())
        assert data['status'] == 400
        assert data['error'] == "Location should be a decimal number and must be filled"

    def test_success_updating_location(self, client, login_user):
        token = login_user
        response = client.patch('/api/v1/1/location', headers=dict(Authorization='Bearer ' + token), content_type='application/json', data=json.dumps(dict(
            location=0.455

        )))
        data = json.loads(response.data.decode())
        assert data['status'] == 200

    def test_success_deleting_id(self, client, login_user):
        token = login_user
        response = client.delete('/api/v1/redflags/1', headers=dict(Authorization='Bearer ' + token))

        data = json.loads(response.data.decode())
        assert data['status'] == 200

    def test_failure_deleting_id(self, client, login_user):
        token = login_user
        response = client.delete('/api/v1/redflags/45', headers=dict(Authorization='Bearer ' + token))

        data = json.loads(response.data.decode())
        assert data['status'] == 400

    def test_first_page(self, client, login_user):
        token = login_user
        response = client.get('api/v1/welcome', headers=dict(Authorization='Bearer ' + token))
        assert response.status_code == 200




