from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from tasks.models import UploadedImage, Tasks
from django.test import Client
from home.models import CustomUser
import random
from unittest.mock import patch
from unittest import mock

User = get_user_model()

class UploadImageTest(TestCase):
    User = get_user_model()
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = Client()
        self.client.login(username="testuser", password="password")
        self.task = Tasks.objects.create(task_name="Test Task", current_progress=10, target=20)

    def test_upload_image(self):
        # Prepare image to upload
        image = SimpleUploadedFile(
            "test_image.jpg", b"image_content", content_type="image/jpeg"
        )
        
        # Simulate image upload for the task
        response = self.client.post(
            reverse("upload_file", args=[self.task.id]),
            {"image": image},
            follow=True
        )
        
        # Check if the image is successfully uploaded
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UploadedImage.objects.filter(task=self.task).exists())

class DeleteImageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = Client()
        self.client.login(username="testuser", password="password")
        self.task = Tasks.objects.create(task_name="Test Task", current_progress=10, target=20)
        self.image = UploadedImage.objects.create(
            task=self.task,
            image="path/to/image.jpg",  # Assuming you've uploaded an image before
            uploaded_by=self.user
        )

    def test_delete_image(self):
        # The image should exist before deletion
        self.assertTrue(UploadedImage.objects.filter(id=self.image.id).exists())
        
        # Simulate image deletion
        response = self.client.post(
            reverse("delete_image", args=[self.image.id]),
            follow=True
        )
        
        # Check if the image is deleted
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UploadedImage.objects.filter(id=self.image.id).exists())

# This tests the Game Master can delete other users photos - the game master main purpose for per reviewing
class GameMasterDeletePhotoTest(TestCase):

    def setUp(self):
        # Create a game master user
        self.game_master = User.objects.create_user(username="GameMaster", password="12345678P")
        self.client = Client()
        self.client.login(username="GameMaster", password="12345678P")
        
        # Create regular user and task
        self.regular_user = User.objects.create_user(username="regularuser", password="12345678P")
        self.task = Tasks.objects.create(task_name="Test Task", current_progress=10, target=20)
        
        # Upload an image for the task
        image = SimpleUploadedFile("test_image.jpg", b"image_content", content_type="image/jpeg")
        self.uploaded_image = UploadedImage.objects.create(
            task=self.task, image=image, uploaded_by=self.regular_user
        )

    def test_game_master_delete_photo(self):
        # The image should exist before deletion
        self.assertTrue(UploadedImage.objects.filter(id=self.uploaded_image.id).exists())
        
        # Simulate the Game Master deleting the image
        response = self.client.post(
            reverse("delete_image", args=[self.uploaded_image.id]),
            follow=True
        )
        
        # Check if the image is deleted
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UploadedImage.objects.filter(id=self.uploaded_image.id).exists())

class TasksViewTest(TestCase):
    """Tests for tasks_view and update_progress"""

    def setUp(self):
        """Set up a user and sample tasks for testing"""
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create multiple tasks
        self.tasks = [
            Tasks.objects.create(task_name=f"Task {i}", completed=False, current_progress=0, target=5)
            for i in range(5)  # More than 3 to check random selection
        ]

        self.original_sample = random.sample

    def test_tasks_view_displays_tasks(self):
        """Test if tasks_view returns tasks for authenticated users"""
        response = self.client.get(reverse("tasks_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("tasks", response.context)
        self.assertLessEqual(len(response.context["tasks"]), 3)

    def test_tasks_view_no_tasks(self):
        """Test if view returns empty list when no incomplete tasks exist"""
        Tasks.objects.all().delete()  # Remove all tasks
        response = self.client.get(reverse("tasks_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tasks"], [])  # Ensuring different tasks

    def test_tasks_progress_increase(self):
        """Test if progress can be increased"""
        task = self.tasks[0]
        response = self.client.post(reverse("update_progress", args=[task.id, "increase"]))
        task.refresh_from_db()

        self.assertEqual(task.current_progress, 1)
        self.assertTrue(response.json()["success"])

    def test_tasks_progress_cannot_exceed_target(self):
        """Test that progress cannot exceed the task's target"""
        task = self.tasks[0]
        task.current_progress = task.target
        task.save()

        response = self.client.post(reverse("update_progress", args=[task.id, "increase"]))
        task.refresh_from_db()

        self.assertEqual(task.current_progress, task.target)  # No change
        self.assertFalse(response.json()["success"])

    def test_tasks_can_be_completed(self):
        """Test that tasks complete when progress reaches target"""
        task = self.tasks[0]
        task.current_progress = task.target - 1
        task.save()

        response = self.client.post(reverse("update_progress", args=[task.id, "increase"]))
        task.refresh_from_db()

        self.assertEqual(task.current_progress, task.target)
        self.assertTrue(task.completed)
        self.assertTrue(response.json()["success"])

    def test_task_cannot_be_claimed_when_unfulfilled(self):
        """Ensure that an unfulfilled task cannot be claimed"""
        task = self.tasks[0]
        response = self.client.post(reverse("update_progress", args=[task.id, "claim"]))
        task.refresh_from_db()

        self.assertFalse(task.completed)
        self.assertFalse(response.json()["success"])

    def test_task_can_be_claimed_when_fulfilled(self):
        """Ensure that a completed task can be claimed"""
        task = self.tasks[0]
        task.current_progress = task.target
        task.has_checked_in = True
        task.save()

        response = self.client.post(reverse("update_progress", args=[task.id, "claim"]))
        task.refresh_from_db()

        self.assertTrue(task.completed)

    def test_task_progress_decreases(self):
        """Ensure that progress can be decreased and task resets"""
        task = self.tasks[0]
        task.current_progress = 3
        task.completed = True
        task.save()

        response = self.client.post(reverse("update_progress", args=[task.id, "decrease"]))
        task.refresh_from_db()

        self.assertEqual(task.current_progress, 2)
        self.assertFalse(task.completed)  # Task should reset
        self.assertTrue(response.json()["success"])