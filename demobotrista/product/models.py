from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    stock = models.PositiveIntegerField(blank=False, null=False)
    currency = models.CharField(
        max_length=3, choices=settings.CURRENCIES, default="TWD"
    )

    class Meta:
        permissions = [
            ("can_manage_products", "Can manage product"),
        ]

    def __str__(self):
        return self.name
