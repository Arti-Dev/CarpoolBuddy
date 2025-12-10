from django import forms
from django.utils import timezone
from .models import Post, DriverReview

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['start_location', 'end_location', 'departure_time', 'num_riders', 'description','photo', 'photo_visibility', 'incentive']
        widgets = {
            'start_location': forms.TextInput(attrs={'placeholder': 'Where are you starting from?'}),
            'end_location': forms.TextInput(attrs={'placeholder': 'Where are you going?'}),
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'num_riders': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'incentive': forms.Textarea(attrs={'rows': 2}),
        }


    #asked chat how to prevent users from picking a time before the current time on 11/20
    #gave me the following methods to add.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the min attribute to NOW so users can’t pick earlier times
        now = timezone.now().strftime("%Y-%m-%dT%H:%M")
        self.fields["departure_time"].widget.attrs["min"] = now

    # Still keep backend validation for safety
    def clean_departure_time(self):
        dep = self.cleaned_data["departure_time"]
        if dep <= timezone.now():
            raise forms.ValidationError("Departure time must be in the future.")
        return dep

class DriverReviewForm(forms.ModelForm):
    class Meta:
        model = DriverReview
        fields = ["comment"]
