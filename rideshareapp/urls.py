from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/add-user/', views.admin_add_user, name='admin-add-user'),
    path('admin/create-cio/', views.admin_create_cio, name='admin-create-cio'),
    path('admin/my-groups/', views.admin_my_groups, name='admin-my-groups'),
    path('cio-dashboard/', views.cio_dashboard, name='cio_dashboard'),
]