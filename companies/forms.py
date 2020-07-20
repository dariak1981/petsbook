from django import forms
from .models import Application, Proposal
from django.conf import settings
User = settings.AUTH_USER_MODEL

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [
            'description'
        ]

class ProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal
        fields = [
            'user_contact', 'title', 'city', 'amount', 'applicants_number', 'description'
        ]
