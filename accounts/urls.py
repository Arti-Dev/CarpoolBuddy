from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.profile_self, name='profile'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path("profileedit/", views.profile_edit, name="profile_edit"),
    path('ban-user', views.ban_user, name='ban_user'),
]