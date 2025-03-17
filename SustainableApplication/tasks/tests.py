from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from tasks.models import UploadedImage, Tasks
from django.test import Client

User = get_user_model()

class UploadImageTest(TestCase):

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

