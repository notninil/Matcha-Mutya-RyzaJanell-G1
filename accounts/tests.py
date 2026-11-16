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

    def test_anonymous_users_must_log_in(self):
        for name in ("dashboard", "explorer_dashboard", "owner_dashboard"):
            with self.subTest(name=name):
                url = reverse(name)
                self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")

    def test_login_routes_by_role_even_with_another_next_url(self):
        for user, destination in (
            (self.explorer, "explorer_dashboard"), (self.owner, "owner_dashboard"),
        ):
            with self.subTest(role=user.role):
                self.client.logout()
                response = self.client.post(
                    reverse("login") + "?next=" + reverse("owner_dashboard"),
                    {"username": user.username, "password": self.password},
                    follow=True,
                )
                self.assertEqual(response.redirect_chain, [
                    (reverse("dashboard"), 302), (reverse(destination), 302),
                ])
                self.assertEqual(response.status_code, 200)

    def test_dashboard_content_navigation_and_role_isolation(self):
        for user, allowed, forbidden, template, content in (
            (self.explorer, "explorer_dashboard", "owner_dashboard",
             "explorer_dashboard.html", "Your matcha trail"),
            (self.owner, "owner_dashboard", "explorer_dashboard",
             "owner_dashboard.html", "Your café business"),
        ):
            with self.subTest(role=user.role):
                self.client.force_login(user)
                response = self.client.get(reverse(allowed))
                self.assertTemplateUsed(response, template)
                self.assertContains(response, content)
                self.assertNotContains(response, reverse(forbidden))
                self.assertEqual(self.client.get(reverse(forbidden)).status_code, 403)
                self.assertEqual(self.client.post(reverse(forbidden), {"role": user.role}).status_code, 403)
                self.assertRedirects(self.client.get(reverse("login")), reverse("dashboard"),
                                     target_status_code=302)

    def test_invalid_login_does_not_create_session(self):
        response = self.client.post(reverse("login"), {
            "username": self.explorer.username, "password": "wrong-password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_requires_post_and_clears_session(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
        url = reverse("owner_dashboard")
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}")
