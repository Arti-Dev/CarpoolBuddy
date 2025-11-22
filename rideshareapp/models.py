from django.db import models
from django.contrib.auth.models import User


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

