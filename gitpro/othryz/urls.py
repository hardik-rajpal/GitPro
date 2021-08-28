from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.signup, name="signup_land"),
    path('submit/', views.makeuser, name="make_user"),
    path('login/', views.loginpage, name="loginpage"),
    path('checkin/', views.checkin, name="checkin")
]
