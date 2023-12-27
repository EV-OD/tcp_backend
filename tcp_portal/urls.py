from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('auth/login/', views.loginUser, name='login'),
    path('auth/register/', views.registerUser, name='register'),

]