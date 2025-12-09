from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/create-cio/', views.admin_create_cio, name='admin-create-cio'),
    path('cio-dashboard/', views.cio_dashboard, name='cio_dashboard'),
    path('report-message/', views.report_message, name='report-message'),
    path('admin/review-flagged-messages/', views.review_flagged_messages, name='review-flagged-messages'),
    path('admin/resolve-flagged-message', views.resolve_flagged_message, name='resolve-flagged-message'),
    path('report-post/', views.report_post, name='report-post'),
    path('admin/review-flagged-posts/', views.review_flagged_posts, name='review-flagged-posts'),
    path('admin/resolve-flagged-post', views.resolve_flagged_post, name='resolve-flagged-post'),
]