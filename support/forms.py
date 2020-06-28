from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(max_length=1000, widget=forms.Textarea(), help_text='Write here your message', required=True)
