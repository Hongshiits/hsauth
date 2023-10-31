"""
URL configuration for hsauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import auth.views
import publicinfo.views

urlpatterns = [
    path('api/auth/register/',auth.views.register),
    path('api/auth/login/',auth.views.login),
    path('api/auth/islogin/',auth.views.islogin),
    path('api/auth/email_otp/',auth.views.email_otp),
    path('api/auth/reset/',auth.views.auth_reset),
    path('api/public/upload_avatar/',publicinfo.views.upload_avatar),
    path('api/public/get_info/',publicinfo.views.get_info),
    path('api/public/update_info/',auth.views.update_info),
    path('api/public/insert_info/',auth.views.insert_info),
    path('api/public/select_info/',auth.views.select_info),
]
