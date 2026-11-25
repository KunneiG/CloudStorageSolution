from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload, name='upload'),
    path('file/<int:pk>/', views.file_detail, name='file_detail'),
    path('file/<int:pk>/download/', views.file_download, name='file_download'),
    path('file/<int:pk>/delete/', views.file_delete, name='file_delete'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='storage/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
