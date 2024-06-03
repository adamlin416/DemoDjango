import json

from django.urls import reverse
from product.models import Product
from rest_framework import status
from rest_framework.test import APITestCase
from user.tests import create_user_get_jwt

# Create your tests here.


class ProductAPITestCase(APITestCase):
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
        self.customer_user, self.customer_token = create_user_get_jwt(
            self.client,
            "test_customer",
            "test@example.com",
            "testpassword",
            25,
            "1234567890",
            False,
        )

    def test_product_list_get(self):
        """customer and manager both can get product list"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("product-list")
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_get(self):
        """customer and manager both can get product list"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("product-detail", kwargs={"pk": product.id})
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create_post(self):
        """test creating a new product, only manager can access"""
        url = reverse("product-list")
        data = {
            "name": "test_product",
            "price": 10,
            "stock": 10,
        }
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(name="test_product")
        self.assertTrue(product)
        self.assertEqual(product.price, 10)
        self.assertEqual(product.stock, 10)

    def test_product_update_put(self):
        """test updating product, only manager can access"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("product-detail", kwargs={"pk": product.id})
        data = {
            "name": "new_product",
            "price": 20,
            "stock": 20,
        }
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "new_product")
        self.assertEqual(product.price, 20)
        self.assertEqual(product.stock, 20)

    def test_product_delete(self):
        """test deleting product, only manager can access"""
        product = Product.objects.create(name="test_product", price=10, stock=10)
        url = reverse("product-detail", kwargs={"pk": product.id})
        # customer
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # manager
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
