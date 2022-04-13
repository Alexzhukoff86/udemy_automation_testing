import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):

    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', json={'username': 'testUser', 'password': 'qwerty'})
                self.assertEqual(request.status_code, 201)
                self.assertDictEqual({'message': 'User created'}, json.loads(request.data))
                self.assertIsNotNone(UserModel.find_by_name('testUser'))

    def test_registered_user_login(self):
        with self.app() as c:
            with self.app_context():
                c.post('/register', json={'username': 'testUser', 'password': 'qwerty'})
                auth_request = c.post('/auth',
                                      json={'username': 'testUser', 'password': 'qwerty'},
                                      headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_registered_user_duplicate(self):
        with self.app() as c:
            with self.app_context():
                c.post('/register', json={'username': 'testUser', 'password': 'qwerty'})

                r = c.post('/register', json={'username': 'testUser', 'password': 'qwerty'})
                self.assertEqual(r.status_code, 400)
                self.assertDictEqual({'message': 'User already exists'}, json.loads(r.data))
