# rideshareapp/forms.py
from django import forms
from .models import CIO, CIOPlaceholderMember


class CIOForm(forms.ModelForm):
    # Text box where you can type: "hey, alice, Bob Smith"
    placeholder_names = forms.CharField(
        required=False,
        label="Initial member names (comma-separated)",
        # help_text='Optional: e.g. "hey, alice, Bob Smith"',
        widget=forms.Textarea(
            attrs={
                "rows": 3,                         # height of the box
                "cols": 30,                        # optional, width
                "placeholder": "hey, alice, Bob Smith",
                "class": "form-control",           # nice Bootstrap styling
            }
        ),
    )

    class Meta:
        model = CIO
        # Only the real model field here; placeholder_names is extra
        fields = ["name"]

    def save(self, commit=True):
        # Create the CIO first
        cio = super().save(commit=commit)

        # Turn the comma-separated string into individual placeholder members
        raw = self.cleaned_data.get("placeholder_names") or ""
        names = [n.strip() for n in raw.split(",") if n.strip()]

        for name in names:
            CIOPlaceholderMember.objects.create(cio=cio, name=name)

        return cio

