import unittest
from unittest.mock import patch
from FlaskApp.app import app
from urllib.parse import urlparse


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

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

    def send_email(self, email):
        return self.app.post('/reset_password', data=dict(
            email=email,
        ), follow_redirects=True)

    #@patch('FlaskApp.app.reset_password_request')
    def test_reset_password_request(self):
        response = self.app.get('/reset_password')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Reset Password" in data
        assert b"Email" in data
        assert b"InterSystems Corporation" in data
        assert b"New Password" not in data
        assert b"Confirm Password" not in data

        rv = self.send_email('duong.do@intersystems.com')
        self.assertEqual(rv.status_code, 302)

        redirect_data = rv.get_data(as_text=True)
        redirect_data = redirect_data.encode('ascii')
        assert b"Welcome to InterSystems Corporation" in redirect_data
        assert b"Instructions to reset your password sent to" in redirect_data
        assert b"duong.do@intersystems.com" in redirect_data
        assert b"Click here to receive container information sending to your email" in redirect_data
        assert b"Click here to reset password" in redirect_data
        assert b"Login" not in redirect_data
        assert b"Logout" not in redirect_data

    def test_reset_password(self):
        response = self.app.get('/reset_password/<user>')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Password" in data
        assert b"InterSystems Corporation" in data
        assert b"Welcome to" not in data
        assert b"Email" not in data

    def test_send_email(self):
        response = self.app.get('/email')
        self.assertEqual(response.status_code, 200)

        data = response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Sent email about container successfully." in data
        assert b"If you want to return to your lab, you can use this link" not in data
        assert b"Reset Password" not in data
        assert b"Confirm Password" not in data

    def test_redirect(self):
        first_response = self.app.get('/a')
        self.assertEqual(first_response.status_code, 302)

        redirect_response = self.app.get('/b')
        data = redirect_response.get_data(as_text=True)
        data = data.encode('ascii')
        assert b"Online Learning Team" in data
        assert b"Reset Password" not in data
        assert b"Confirm Password" not in data
