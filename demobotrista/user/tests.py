import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


def create_user_get_jwt(client, username, email, password, age, phone, is_manager):
    """
    Create a user and get jwt token for the user. Return user and token.
    Will be called in setUp method for all test cases.
    """
    # make sure group and perms exist
    call_command("manage_groups")
    # create user and get jwt token
    jwt_create_url = reverse("token_obtain_pair")
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        age=age,
        phone=phone,
        is_staff=is_manager,
    )
    group, _ = Group.objects.get_or_create(name="Manager" if is_manager else "Customer")
    group.user_set.add(user)
    resp = client.post(
        jwt_create_url, {"username": username, "password": password}, format="json"
    )
    acc_toekn = resp.json()["data"]["access"]
    return user, acc_toekn


class UserAPITestCase(APITestCase):
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

    def test_user_create_post(self):
        """test creating a new user."""
        url = reverse("user-list")
        data = {
            "username": "test_user_post",
            "password": "newpassword",
            "is_manager": False,
        }
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="test_user_post")
        self.assertTrue(user)
        self.assertTrue(user.check_password("newpassword"))

    def test_user_list_get(self):
        """test getting list of users, only manager can access"""
        url = reverse("user-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manager_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_get(self):
        """only allow detail from himself"""
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # access other user's detail should be forbidden
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_put(self):
        """test updating user"""
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id})
        data = {
            "username": "new_username",
            "password": "newpassword",
        }
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer_user.refresh_from_db()
        self.assertEqual(self.customer_user.username, "new_username")
        self.assertTrue(self.customer_user.check_password("newpassword"))

        # should not allow updating other user
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id + 1})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # should not allow empty data
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id})
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete(self):
        # test deleting user
        url = reverse("user-detail", kwargs={"pk": self.customer_user.id})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.customer_token}")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.customer_user.id).exists())
