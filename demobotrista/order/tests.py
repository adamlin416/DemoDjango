import json

from django.urls import reverse
from order.models import Order
from product.models import Product
from rest_framework import status
from rest_framework.test import APITestCase
from user.tests import create_user_get_jwt

# Create your tests here.


class OrderAPITestCase(APITestCase):
    def setUp(self):
        # create one manager and exchange for token
        self.manager_user, self.manager_token = create_user_get_jwt(
            self.client,
            "test_manager",
            "test@example.com",
            "testpassword",
            25,
            "1234567890",
            True,
        )
        self.customer_user_1, self.customer_token_1 = create_user_get_jwt(
            self.client,
            "test_customer",
            "test@example.com",
            "testpassword",
            25,
            "1234567890",
            False,
        )
        self.customer_user_2, self.customer_token_2 = create_user_get_jwt(
            self.client,
            "test_customer_2",
            "test@example.com",
            "testpassword",
            25,
            "1234567890",
            False,
        )

    def test_order_list_get(self):
        """customer list his own orders, manager list all orders"""
        Order.objects.create(
            user=self.customer_user_1,
        )
        Order.objects.create(
            user=self.customer_user_2,
        )
        url = reverse("order-list")
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token_1}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("data")), 1)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("data")), 2)

    def test_create_order(self):
        """test creating a new order, only customer can access"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("order-list")
        data = {
            "items": [
                {
                    "product": product.id,
                    "quantity": 5,
                }
            ]
        }
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token_1}")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check if stock is reduced
        product.refresh_from_db()
        self.assertEqual(product.stock, 5)
        # check if order is created
        order = Order.objects.get(user=self.customer_user_1)
        self.assertTrue(order)
        self.assertEqual(order.items.count(), 1)
        order_item = order.items.first()
        self.assertEqual(order_item.product, product)
        self.assertEqual(order_item.quantity, 5)

    def test_create_order_stock_not_enough(self):
        """test creating a new order, only when stock is enough"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("order-list")
        data = {
            "items": [
                {
                    "product": product.id,
                    "quantity": 15,
                }
            ]
        }
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token_1}")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check if stock is not reduced
        product.refresh_from_db()
        self.assertEqual(product.stock, 10)
        # check if order is not created
        self.assertFalse(Order.objects.filter(user=self.customer_user_1).exists())
