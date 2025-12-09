from django.db import models
from django.contrib.auth.models import User

from chat.models import ChatRoom


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    computing_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Spring 5 Requirements Change addition
    nickname = models.CharField(max_length=20, blank=True, null=True)
    sustainability_interests = models.TextField()
    onboarded = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_groups(self) -> str:
        # Asked ChatGPT on how to obtain groups that a user is in
        groups = self.user.groups.values_list('name', flat=True)
        return ", ".join(groups)

    def get_accessible_rooms(self):
        rooms = ChatRoom.objects.filter(chataccess__user=self.user.profile).distinct()
        return [{"id": room.id, "title": room.title} for room in rooms]
    
    def get_display_name(self):
        if self.nickname and self.nickname.strip():
            return self.nickname
        return self.user.first_name
