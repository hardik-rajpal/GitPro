from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('checkin/', views.checkin, name="checkin"),
    path('register/', views.register, name="register")
]
