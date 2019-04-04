import unittest
from unittest.mock import patch
import codecs
from urllib.parse import urlparse
from FlaskApp.app import app
from FlaskApp.forms import ResetPasswordRequestForm, ResetPasswordForm


class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Welcome to InterSystems Corporation" in data
        assert b"Contents:" in data
        assert b"Click here to receive container information sending to your email" in data
        assert b"Click here to reset password" in data
        assert b"Login" not in data
        assert b"Logout" not in data

    def test_reset_password_request_get(self):
        response = self.app.get('/reset_password')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Reset Password" in data
        assert b"Email" in data
        assert b"InterSystems Corporation" in data
        assert b"New Password" not in data
        assert b"Confirm Password" not in data

    @patch('FlaskApp.app.send_password_reset_email')
    def test_reset_password_request_post(self, mock_send):
        response = self.app.post(
            '/reset_password',
            data={'email': 'fake_email@example.com'})
        self.assertEqual(response.status_code, 302)
        assert response.location.endswith('/')

    @patch('FlaskApp.app.send_password_reset_email')
    def test_reset_password_request_post_invalid(self, mock_send):
        response = self.app.post(
            '/reset_password',
            data={'email': 'wrong_email'})
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Reset Password" in data

    def test_reset_password_get(self):
        response = self.app.get('/reset_password/fake_user')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Password" in data
        assert b"InterSystems Corporation" in data
        assert b"Welcome to" not in data
        assert b"Email" not in data

    @patch('FlaskApp.app.set_password')
    def test_reset_password_post(self, mock_set):
        response = self.app.post(
            '/reset_password/fake_user',
            data={'password': 'fake_password', 'password2': 'fake_password'})
        self.assertEqual(response.status_code, 302)
        assert response.location.endswith('/')

    @patch('FlaskApp.app.set_password')
    def test_reset_password_post_invalid(self, mock_set):
        response = self.app.post(
            '/reset_password/fake_user',
            data={'password': 'fake_password', 'password2': 'wrong_password'})
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Password" in data

    @patch('FlaskApp.app.send_async_email')
    def test_send_email(self, mock_send):
        response = self.app.get('/email')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Sent email about container successfully." in data
        assert b"If you want to return to your lab, you can use this link" not in data
        assert b"Reset Password" not in data
        assert b"Confirm Password" not in data


