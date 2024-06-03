from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""

    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        permissions = [
            ("can_list_users", "Can list users"),
        ]
