# rideshareapp/forms.py
from django import forms
from .models import CIO, CIOPlaceholderMember

class CIOForm(forms.ModelForm):
    initial_member_name = forms.CharField(
        required=False,
        label="Initial member name",
        help_text='Optional: e.g. "hey"',
        widget=forms.TextInput(attrs={"placeholder": "Enter a member name"}),
    )

    class Meta:
        model = CIO
        fields = ["name"]  # just the CIO name from the model

    def save(self, commit=True):
        cio = super().save(commit=commit)

        # Single member name instead of comma-separated list
        member_name = self.cleaned_data.get("initial_member_name", "").strip()

        if member_name:
            CIOPlaceholderMember.objects.create(cio=cio, name=member_name)

        return cio
