from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('profile/', views.profile_self, name='profile'),
    # asked chat to help me make profile url that takes user id as argument on 12/8/25
    path('profile/<int:user_id>', views.profile, name='profile'),
    path("profileedit/", views.profile_edit, name="profile_edit"),
    path('ban-user', views.ban_user, name='ban_user'),
    path('delete-account/', views.delete_account, name='delete_account')
]