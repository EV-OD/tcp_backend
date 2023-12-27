from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.reportPage, name='reportPage'),
    path('search/<str:ip>/', views.searchPage, name='searchPage'),
    path('login/', views.loginPage, name='loginPage'),
    path('register/', views.registerPage, name='registerPage'),
    path('auth/login/', views.loginUser, name='login'),
    path('auth/register/', views.registerUser, name='registerUser'),
    path('auth/logout/', views.logoutUser, name='logout'),
    path('autoflag/', views.autoflagPage, name='autoflagPage'),
    path('setpublicflag/', views.setPublicFlag, name='setPublicFlag'),
    path('setauthflag/', views.setAuthFlag, name='setauthflag'),
]