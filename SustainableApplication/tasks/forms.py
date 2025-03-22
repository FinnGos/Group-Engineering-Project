from django import forms
from .models import UploadedImage, Tasks

"""
This module defines a Django form for uploading images and associating them with a task.

Classes:
    ImageUploadForm: A ModelForm that allows users to upload an image and associate it with a specific task.

Attributes:
    task (ModelChoiceField): A dropdown field that allows users to select a task from all available tasks.
    image (ImageField): The image file that the user uploads.

Meta:
    model (UploadedImage): Specifies that the form is based on the UploadedImage model.
    fields (list): Defines the fields that should be included in the form ('task' and 'image').

Usage:
    This form is used in views to handle user uploads and ensure the image is linked to a task.
"""

class ImageUploadForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Tasks.objects.all(), label="Select Task")

    class Meta:
        model = UploadedImage
        fields = ['task', 'image']
