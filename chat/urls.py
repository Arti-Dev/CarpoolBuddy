from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="chatindex"),
    path('start_chat/', views.start_chat, name='start-chat'),
    path('start_group_chat/', views.start_group_chat, name='start-group-chat'),
    path("<int:room_id>/", views.room_view, name="room"),
    path("validate_other_user/", views.validate_other_user, name="validate-other-user"),
]