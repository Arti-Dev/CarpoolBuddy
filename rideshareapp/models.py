from django.db import models
from django.contrib.auth.models import User

from accounts.models import Profile
from posts.models import Post


class CIO(models.Model):
    name = models.CharField(max_length=100)
    # real users who have actually joined this CIO
    members = models.ManyToManyField(User, blank=True, related_name='cios')

    def __str__(self):
        return self.name


class CIOPlaceholderMember(models.Model):
    cio = models.ForeignKey(CIO, on_delete=models.CASCADE, related_name='placeholder_members')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (placeholder for {self.cio.name})"

class ReportedMessage(models.Model):
    message = models.TextField()
    room = models.TextField()
    message_author_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    reason = models.TextField(blank=True)

class ReportedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)