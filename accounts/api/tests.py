from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = self.createUser(
            username='admin1',
            email='admin1@jiuzhang.com',
            password='correct password',
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # Use GET instead of POST
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 405)

        # Use POST, wrong username
        response = self.client.post(LOGIN_URL, {
            'username': "wrong",
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 400)
        # Not Logged in yet
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # Use POST, wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 400)

        # Not Logged in yet
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # Use POST, right username and password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], 'admin1')
        self.assertEqual(response.data['user']['email'], 'admin1@jiuzhang.com')
        # Logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'hy2610',
            'password': '12345678',
            'email': 'hy2610@jiuzhang.com',
        }

        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        response = self.client.post(SIGNUP_URL, {
            'username': 'hy26101111111111111111111111111111111111',
            'password': '12345678',
            'email': 'hy2610@jiuzhang.com',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(SIGNUP_URL, {
            'username': 'hy2610',
            'password': '123',
            'email': 'hy2610@jiuzhang.com',
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'hy2610')

        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)








