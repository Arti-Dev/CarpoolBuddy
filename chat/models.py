from django.db import models

class ChatRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    dm = models.BooleanField(default=False)

class ChatAccess(models.Model):
    user = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

# If a user has unread messages, there will be an entry here
# Once a user enters the room remove this entry
class RoomUnread(models.Model):
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
