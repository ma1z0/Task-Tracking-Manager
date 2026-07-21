from rest_framework.test import APITestCase
from tasks.models import Task
from rest_framework import status
from django.contrib.auth import get_user_model

class TaskAPITests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.owner = User.objects.create_user("owner")
        self.assignee = User.objects.create_user("assignee")
        self.other_user = User.objects.create_user("other_user")

        self.task = Task.objects.create(
            title = 'test_task',
            description = 'dasdasd',
            owner = self.owner,
            assignee = self.assignee,
        )

    def test_owner_can_retrieve_task(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assignee_can_retrieve_assigned_task(self):
        self.client.force_authenticate(user=self.assignee)
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unrelated_user_cannot_retrieve_task(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_task_title(self):
        self.client.force_authenticate(user=self.owner)
        data = {"title": "updated title"}
        response = self.client.patch(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "updated title")

    def test_assignee_can_update_task_status(self):
        self.client.force_authenticate(user=self.assignee)
        data = {"status": Task.Status.IN_PROGRESS}
        response = self.client.patch(f"/api/tasks/{self.task.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)

    def test_assignee_cannot_update_task_title(self):
        self.client.force_authenticate(user=self.assignee)
        data = {"title": "updated_2 title"}
        response = self.client.patch(f"/api/tasks/{self.task.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "test_task")

    def test_assignee_cannot_delete_task(self):
        self.client.force_authenticate(user=self.assignee)
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.task.refresh_from_db()
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_authenticated_user_can_create_task(self):
        self.client.force_authenticate(user=self.owner)
        data = {"title": "created_task_2"}
        before_new_task = Task.objects.count()
        response = self.client.post(f"/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        after_new_task = Task.objects.count()
        self.assertEqual(after_new_task, before_new_task + 1)
        created_task = Task.objects.get(title = "created_task_2")
        self.assertEqual(created_task.owner, self.owner)

    def test_unauthorized_user_cannot_create_task(self):
        data = {"title": "unauthorized_task"}
        before_new_task = Task.objects.count()
        response = self.client.post(f"/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        after_new_task = Task.objects.count()
        self.assertEqual(before_new_task, after_new_task)