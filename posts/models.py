from django.db import models
from django.contrib.auth.models import User

#asked chat how to implement photo visibility on 12/8/25
#gave me the following class to add 
class Photo_visibility(models.TextChoices):
    PUBLIC = "Public", "Can be seen by anyone"
    PRIVATE = "Private", "I can only see it"
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    num_riders = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to="post_photos/", null=True, blank=True)

    photo_visibility = models.CharField(
        max_length=10,
        choices=Photo_visibility.choices,
        default=Photo_visibility.PUBLIC,
    )

    description = models.TextField(blank=True)
    incentive = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    #asked chat to help me implement the 0 or 1 CIO set up on 12/9/25
    cio = models.ForeignKey("rideshareapp.CIO",on_delete=models.SET_NULL,null=True,blank=True,related_name="posts")
    
    def __str__(self):
        return f"{self.author.username}: {self.start_location} to {self.end_location} at {self.departure_time.strftime('%b %d %I:%M %p')}"
    
    @property
    def author_display_name(self):
        return self.author.profile.get_display_name()
    #asked chat how to implement photo visibility on 12/8/25
    #gave me the following method and I adjsted to my needs
    def can_view_photo(self, user):
        if self.photo_visibility == Photo_visibility.PUBLIC:
            return True
        if user == self.author:
            return True
        return False

