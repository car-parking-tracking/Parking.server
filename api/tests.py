from unittest import skip
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


from parking_backend import settings

User = get_user_model()


@skip
class EmailVerificationTest(APITestCase):
    base_url = settings.BASE_URL
    register_url = f'http://localhost{base_url}'
    activate_url = f"{base_url}activation/"
    login_url = "/api/v1/auth/token/login/"
    user_details_url = base_url

    user_data = {
        "first_name": "Name",
        "last_name": "Surname",
        "email": "test@example.com",
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


class UrlTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test1@test.ru', 
            password = 'verysecret1'
            )
        self.token = Token.objects.create(user=self.user)

    def test_feature_collection(self):
        url = 'http://localhost/api/v1/feature_collection/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parking_lots(self):
        url = 'http://localhost/api/v1/parking_lots/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_authorized_users_get(self):
        list_url = reverse('user-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_users_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_authorized_user_patch(self):
        update_data = {"email": "test3@test.ru"}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('user-detail', kwargs={'id': self.user.id})
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['email'], update_data['email'])
        self.client.credentials()

    def test_authorized_user_delet(self):
        new_user = User.objects.create_user(email='test2@test.ru', password='verysecret2')
        new_user_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {new_user_token.key}')
        data = {'current_password': 'verysecret2'}
        url = reverse('user-me')
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_authorized_user_delet(self):
        user_to_delete = User.objects.create_user(email='test3@test.ru', password = 'verysecret3')
        user_to_delete_id = user_to_delete.id
        self.client.credentials()
        url = reverse('user-detail', kwargs={'id': user_to_delete_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_set_password(self):
        password_data = {'new_password': 'verysecret3',
                         'current_password': 'verysecret1'
                         }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('user-set-password')
        response = self.client.post(url, data=password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
