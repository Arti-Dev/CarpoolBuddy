from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="chatindex"),
    path('start_chat/', views.start_chat, name='start-chat'),
    path("<str:room_name>/", views.room, name="room"),
]