from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['start_location', 'end_location', 'departure_time', 'num_riders', 'description']
        widgets = {
            'start_location': forms.TextInput(attrs={'placeholder': 'Where are you starting from?'}),
            'end_location': forms.TextInput(attrs={'placeholder': 'Where are you going?'}),
            'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'num_riders': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
