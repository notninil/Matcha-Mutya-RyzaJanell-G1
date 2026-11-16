from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountTests(TestCase):
    password = "Matcha!trail-journey-406"

    def setUp(self):
        self.explorer = User.objects.create_user("explorer", "explorer@example.com", self.password)
        self.owner = User.objects.create_user(
            "owner", "owner@example.com", self.password, role=User.Role.OWNER,
        )
        self.registration = {
            "username": "newexplorer", "email": "new@example.com",
            "password1": self.password, "password2": self.password,
        }

    def test_registration_hashes_password_and_ignores_submitted_role(self):
        response = self.client.post(reverse("register"), {**self.registration, "role": "owner"})
        self.assertRedirects(response, reverse("register"))
        user = User.objects.get(username="newexplorer")
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertEqual(user.role, User.Role.EXPLORER)

    def test_registration_validation(self):
        for field, value in [
            ("username", ""), ("username", "Explorer"), ("email", "invalid"),
            ("email", "OWNER@EXAMPLE.COM"), ("password2", "different"),
        ]:
            with self.subTest(field=field, value=value):
                response = self.client.post(reverse("register"), {**self.registration, field: value})
                self.assertIn(field, response.context["form"].errors)
                self.assertEqual(User.objects.count(), 2)
