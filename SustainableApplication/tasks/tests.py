from django.test import TestCase
from django.urls import reverse
from .models import Tasks
from django.utils.timezone import now, timedelta
from home.models import CustomUser


class TaskViewTests(TestCase):
    def setUp(self):
        """Set up test user and task"""
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.task = Tasks.objects.create(
            task_name="Test Task", current_progress=0, target=10, completed=False
        )

    def test_task_view(self):
        """Test that at least one task is displayed if there are incomplete tasks"""
        response = self.client.get(reverse("tasks_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")  # ensure a task is shown

    def test_update_progress_increase(self):
        """Test increasing task progress"""
        response = self.client.post(
            reverse("update_progress", args=[self.task.id, "increase"])
        )
        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.task.current_progress, 1)

    def test_invalid_update_action(self):
        """Test an invalid action"""
        response = self.client.post(
            reverse("update_progress", args=[self.task.id, "invalid_action"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["message"], "Invalid action or limit reached.")

    def test_progress_resets_after_day_change(self):
        """Test that the progress of a task resets after a day passes"""
        self.task.updated_at = now() - timedelta(days=1)
        self.task.save()

        response = self.client.get(reverse("tasks_view"))
        self.task.refresh_from_db()

        self.assertEqual(self.task.current_progress, 0)
