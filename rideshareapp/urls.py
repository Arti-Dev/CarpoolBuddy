from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('moderator/', views.moderator, name='moderator'),
    path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),
    path('admin/add-user/', views.admin_add_user, name='admin-add-user'),
    path('admin/create-event/', views.admin_create_event, name='admin-create-event'),
    path('admin/my-groups/', views.admin_my_groups, name='admin-my-groups')
]