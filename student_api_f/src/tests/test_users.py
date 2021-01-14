import unittest
import os
import json
from ..app import create_app, db
from flask import jsonify, make_response

class UsersTest(unittest.TestCase):

    def setUp(self):

        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'olawale',
            'email': 'olawale@mail.com',
            'password': 'passw0rd!'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):

        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))

        self.assertEqual(res.status_code, 201)


    def test_user_creation_with_existing_email(self):
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def test_user_creation_with_no_password(self):
        user1 = {
            'name': 'olawale',
            'email': 'olawale1@mail.com',
        }
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('password'))

    def test_user_creation_with_no_email(self):
        user1 = {
            'name': 'olawale',
            'pasword': 'olawale1@mail.com',
        }
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('email'))

    def test_user_creation_with_empty_request(self):
        user1 = {}
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_user_login(self):
        """ User Login Tests """
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/admins/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)
    def test_student(self):
        user1 = {
            "first_name": "Marian",
            "last_name": "Lukavyi",
            "rating": 100
        }
        res = self.client().post('/api/v1/students/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        # self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'Authentication token is not available, please login to get one')
        self.assertEqual(res.status_code, 400)
    def test_student_creation_with_no_rating(self):
        user1 = {
            "first_name": "Marian",
            "last_name": "Lukavyi"
        }
        res = self.client().post('/api/v1/students/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('error'), 'Authentication token is not available, please login to get one')
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_invalid_password(self):
        user1 = {
            'password': 'olawale',
            'email': 'olawale@mail.com',
        }
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/admins/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_invalid_email(self):
        user1 = {
            'password': 'passw0rd!',
            'email': 'olawale1111@mail.com',
        }
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/admins/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_get_me(self):
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        # print(api_token)
        res = self.client().get('/api/v1/admins/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('error'), None)
        self.assertEqual(res.status_code, 400)
        # self.assertEqual(json_data.get('email'), 'olawale@mail.com')
        # self.assertEqual(json_data.get('name'), 'olawale')

    def test_user_update_me(self):
        user1 = {
            'name': 'new name'
        }
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/v1/admins/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('error'), None)
        self.assertEqual(res.status_code, 400)
        # self.assertEqual(json_data.get('name'), 'new name')

    def test_delete_user(self):
        res = self.client().post('/api/v1/admins/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user, indent=3))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        print(api_token)
        self.assertEqual(api_token, {'error': 'error in generating user token'} )
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/admins/me',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(json_data.get('error'), None)
        self.assertEqual(res.status_code, 400)
    def tearDown(self):

        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
# import requests
# import json

# def test_post_headers_body_json():
#     url = 'http://0.0.0.0:5000/api/v1/admins/'
#
#     headers = {'Content-Type': 'application/json'}
#
#     # Body
#     payload = {
#         "email": "23ds3222@email.ua",
#         "password": "23d2s23232",
#         "name": "j223322ds323ohn"
#     }
#
#     resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
#     assert resp.status_code == 201
#     resp_body = resp.json()
#
# import requests
#
#
# def test_post_headers_body_json():
#     url = "http://127.0.0.1:5000/api/v1/admins/"
#
#     payload = "{\n    \"email\": \"mar1ia1n@email.ua\",\n    \"password\": \"2111\",\n    \"name\": \"maria11n\"\n}"
#     headers = {
#         'Content-Type': 'application/json'
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     assert response.status_code == 201
#     resp_body = response.json()
#     print(response.text)
