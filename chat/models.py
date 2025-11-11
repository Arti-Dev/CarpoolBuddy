from django.db import models

from accounts.models import Profile

class ChatRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)

class ChatAccess(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
