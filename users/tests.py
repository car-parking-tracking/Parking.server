from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersManagersTest(TestCase):
    """
    Тестирование создания пользователя и
    суперпользователя.
    """

    def test_create_user(self):
        """
        Создание пользователя без лишних прав.
        """
        
        user = User.objects.create(email='user@user.com', password='12345')
        self.assertEqual(user.email, 'user@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="12345")

    def test_create_superuser(self):
        """
        Создание суперпользователя с корректными правами.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="12345"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="12345", is_superuser=False)
