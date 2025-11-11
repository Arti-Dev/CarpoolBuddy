from django import forms

class DirectMessageForm(forms.Form):
    recipient = forms.CharField(max_length=50)
