from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    num_riders = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to="post_photos/", null=True, blank=True)

    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.start_location} to {self.end_location} at {self.departure_time.strftime('%b %d %I:%M %p')}"
    
    @property
    def author_display_name(self):
        return self.author.profile.get_display_name()

