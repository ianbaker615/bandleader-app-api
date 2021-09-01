from django.test import TestCase  # pylint: disable=import-error
from django.contrib.auth import get_user_model  # pylint: disable=import-error


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        # New user with email is created
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        # Email for new user is normalized
        email = "test@GMAIL.COM"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        # Creating user with no email raises error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        # New superuser is created
        user = get_user_model().objects.create_superuser(
            "superusertest@gmail.com", "test123"
        )

        # .is_superuser is included as part of PermissionsMixins \
        # which the User class is extending in ./app/app/models.py
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
