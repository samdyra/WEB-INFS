import os

from django import forms

from .models import GeoDataProject
from .validators import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


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


class GeoJSONUploadForm(forms.Form):
    file = forms.FileField(
        label='GeoJSON file',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.geojson,.json,application/geo+json,application/json',
        }),
    )

    def clean_file(self):
        f = self.cleaned_data['file']

        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise forms.ValidationError(
                'File must be a .geojson or .json file.'
            )

        if f.size > MAX_FILE_SIZE:
            raise forms.ValidationError(
                f'File is too large ({f.size / (1024 * 1024):.1f} MB). '
                f'Maximum size is {MAX_FILE_SIZE // (1024 * 1024)} MB.'
            )

        return f
