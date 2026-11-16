from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    class Role(models.TextChoices):
        EXPLORER = "explorer", "Explorer"
        OWNER = "owner", "Café Owner"

    email = models.EmailField()
    role = models.CharField(max_length=10, choices=Role, default=Role.EXPLORER)
    contact_number = models.CharField(max_length=32, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="accounts_email_ci_unique"),
            models.UniqueConstraint(Lower("username"), name="accounts_username_ci_unique"),
            models.CheckConstraint(
                condition=models.Q(role__in=["explorer", "owner"]),
                name="accounts_valid_role",
            ),
        ]
