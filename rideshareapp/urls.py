from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('moderator/', views.moderator, name='moderator'),
    path('cio-dashboard/', views.cio_dashboard, name='cio_dashboard'),
]