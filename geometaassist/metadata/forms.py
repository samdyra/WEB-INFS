import json

from django import forms

from .models import MetadataRecord


class MetadataRecordForm(forms.ModelForm):
    keywords_input = forms.CharField(
        required=False,
        label='Keywords',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'flood, hydrology, Queensland',
        }),
        help_text='Comma-separated list of keywords',
    )

    providers_input = forms.CharField(
        required=False,
        label='Providers',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        help_text=(
            'JSON array of provider objects. Example: '
            '[{"name": "Queensland Government", "roles": ["producer", "host"]}]'
        ),
    )

    links_input = forms.CharField(
        required=False,
        label='Links',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        help_text=(
            'JSON array of link objects. Example: '
            '[{"href": "https://example.com", "rel": "related", "title": "Source"}]'
        ),
    )

    class Meta:
        model = MetadataRecord
        fields = [
            'stac_item_id', 'title', 'description',
            'datetime_start', 'datetime_end',
            'license',
        ]
        widgets = {
            'stac_item_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. brisbane-flood-extent-2023',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Brisbane Flood Extent 2023',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'datetime_start': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'datetime_end': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'license': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ('datetime_start', 'datetime_end'):
            self.fields[f].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']

        instance = kwargs.get('instance')
        if instance:
            if instance.keywords:
                self.fields['keywords_input'].initial = ', '.join(instance.keywords)
            if instance.providers:
                self.fields['providers_input'].initial = json.dumps(instance.providers, indent=2)
            if instance.links:
                self.fields['links_input'].initial = json.dumps(instance.links, indent=2)

    def clean_keywords_input(self):
        raw = self.cleaned_data.get('keywords_input', '')
        if not raw.strip():
            return []
        return [k.strip() for k in raw.split(',') if k.strip()]

    def clean_providers_input(self):
        raw = self.cleaned_data.get('providers_input', '').strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON. Please check the format.')
        if not isinstance(parsed, list):
            raise forms.ValidationError('Providers must be a JSON array.')
        return parsed

    def clean_links_input(self):
        raw = self.cleaned_data.get('links_input', '').strip()
        if not raw:
            return []
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON. Please check the format.')
        if not isinstance(parsed, list):
            raise forms.ValidationError('Links must be a JSON array.')
        return parsed

    def save(self, commit=True):
        record = super().save(commit=False)
        record.keywords = self.cleaned_data['keywords_input']
        record.providers = self.cleaned_data['providers_input']
        record.links = self.cleaned_data['links_input']
        if commit:
            record.save()
        return record
