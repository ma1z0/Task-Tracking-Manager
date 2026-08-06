from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


class RegistrationAPITests(APITestCase):
    def test_user_can_register(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_class = get_user_model()
        created_user = user_class.objects.get(username=data["username"])
        self.assertEqual(created_user.username, data["username"])
        self.assertTrue(created_user.check_password(data["password"]))
        self.assertNotIn("password", response.data)
