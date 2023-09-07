from unittest import skip

from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

from parking_backend import settings


@skip
class EmailVerificationTest(APITestCase):
    base_url = settings.BASE_URL
    register_url = base_url
    activate_url = f"{base_url}activation/"
    login_url = "/api/v1/auth/token/login/"
    user_details_url = base_url

    user_data = {
        "email": "test@example.com",
        "username": "test_user",
        "password": "verysecret"
    }
    login_data = {
        "email": "test@example.com",
        "password": "verysecret"
    }

    def test_user_register_with_email_verification(self):
        response = self.client.post(
            path=self.register_url,
            data=self.user_data,
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(len(mail.outbox), 1)

        email_lines = mail.outbox[0].body.splitlines()

        activation_link = [
            line for line in email_lines if "/activate/" in line
        ][0]
        uid, token = activation_link.split("/")[-2:]
        data = {"uid": uid, "token": token}

        response = self.client.post(
            path=self.activate_url, data=data
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        response = self.client.post(
            path=self.login_url, data=self.login_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'auth_token')
        token = response.json().get('auth_token')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get(path=self.user_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['email'], self.user_data['email'])
