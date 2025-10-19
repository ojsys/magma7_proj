from django import forms
from .models import Subscription


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = []  # plan chosen in view; no direct fields needed

