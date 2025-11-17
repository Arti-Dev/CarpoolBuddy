from django.contrib import admin

from .models import Profile
from posts.models import Post
admin.site.register(Profile)
admin.site.register(Post)
