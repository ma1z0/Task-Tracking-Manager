from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status


class RegistrationAPITests(APITestCase):
    def test_user_can_register(self):
        data = {"username": "test", "password": "fdsme#MfimO#00@93#0#_"}
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_class = get_user_model()
        created_user = user_class.objects.get(username=data["username"])
        self.assertEqual(created_user.username, data["username"])
        self.assertTrue(created_user.check_password(data["password"]))
        self.assertNotIn("password", response.data)

    def test_registration_rejects_duplicate_username(self):
        User = get_user_model()

        User.objects.create_user(
            username="test",
            password="fdsme#MfimO#00@93#0#_",
        )

        data = {"username": "test", "password": "fdsme#MfimO#00@93#0#_"}

        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        users_count = User.objects.filter(username="test").count()
        self.assertEqual(users_count, 1)

    def test_registration_rejects_weak_password(self):
        User = get_user_model()
        data = {"username": "ma1z0", "password": "123"}

        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        users_count = User.objects.filter(username="ma1z0").count()
        self.assertEqual(users_count, 0)
