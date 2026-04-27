from django import forms

from .models import GeoDataProject


class GeoDataProjectForm(forms.ModelForm):
    class Meta:
        model = GeoDataProject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Brisbane Flood Extent 2023',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the purpose of this project and the datasets it will contain...',
            }),
        }
        labels = {
            'name': 'Project Name',
            'description': 'Description',
        }
