from django.test import TestCase
from django.urls import reverse
from .models import Tasks
from django.utils.timezone import now, timedelta


class TaskViewTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.task1 = Tasks.objects.create(
            task_name="Test Task 1",
            current_progress=0,
            target=5,
            completed=False,
            has_checked_in=True,
        )
        self.task2 = Tasks.objects.create(
            task_name="Test Task 2",
            current_progress=4,
            target=4,
            completed=True,
            has_checked_in=True,
        )

    def test_task_view(self):
        """Test that at least one task is displayed if there are incomplete tasks"""
        response = self.client.get(reverse("tasks_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task")  # ensure a task is shown

    def test_update_progress_increase(self):
        """Test increasing task progress"""
        response = self.client.post(
            reverse("update_progress", args=[self.task1.id, "increase"])
        )
        self.task1.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.task1.current_progress, 1)

    def test_update_progress_claim(self):
        """Test claiming a completed task"""
        response = self.client.post(
            reverse("update_progress", args=[self.task1.id, "claim"])
        )
        self.task1.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertTrue(self.task1.completed)

    def test_invalid_update_action(self):
        """Test an invalid action"""
        response = self.client.post(
            reverse("update_progress", args=[self.task1.id, "invalid_action"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["message"], "Invalid action or limit reached.")

    def test_progress_resets_after_day_change(self):
        """Test that the progress of a task resets after a day passes"""
        self.task1.updated_at = now() - timedelta(days=1)
        self.task1.save()

        response = self.client.get(reverse("tasks_view"))
        self.task1.refresh_from_db()

        self.assertEqual(self.task1.current_progress, 0)

    def test_no_tasks_shown_if_all_completed(self):
        """Test that no tasks are displayed if all are completed"""

        self.task1.copmpleted = True
        self.task2.completed = True
        self.task1.save()
        self.task2.save()

        response = self.client.get(reverse("tasks_view"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response, "No tasks available to complete."
        )  # ensure no tasks are shown
