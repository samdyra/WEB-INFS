from django import forms

from .models import SubscriptionPlan, UserSubscription


class StaffSubscriptionForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    status = forms.ChoiceField(
        choices=UserSubscription.Status.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = UserSubscription
        fields = ('plan', 'status')
