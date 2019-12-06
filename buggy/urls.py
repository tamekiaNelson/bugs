"""buggy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from buggy import views
from buggy.models import Bugs
# admin.site.register(buggy)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('login/', views.loginview),
    url('', views.index),
    url('list/', views.mainlist),
    url('ticket/', views.view_single_ticket),
    url('add/', views.add),
    url('edit/', views.edit),
    url('logout/', views.logoutview),
    ]
