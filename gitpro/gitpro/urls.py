"""gitpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import re_path
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, include
from othryz import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.checkin),
    path('profile/<str:profile_username>/', views.profile),
    path('update/', views.updateProfile),
    path('accounts/', include('othryz.urls')),
    path('explore/', views.explore),
    path('error/', views.error),
    re_path(r'^.*$', RedirectView.as_view(url='/dashboard/', permanent=False), name='catchall')
    # path('accounts/', include('django.contrib.auth.urls')),
]
