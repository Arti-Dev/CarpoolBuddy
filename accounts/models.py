from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def get_groups(self) -> str:
        # Asked ChatGPT on how to obtain groups that a user is in
        groups = self.user.groups.values_list('name', flat=True)
        return ", ".join(groups)