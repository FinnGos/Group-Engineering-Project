from django import forms
from .models import UploadedImage, Tasks

class ImageUploadForm(forms.ModelForm):
    task = forms.ModelChoiceField(queryset=Tasks.objects.all(), label="Select Task")

    class Meta:
        model = UploadedImage
        fields = ['task', 'image']
