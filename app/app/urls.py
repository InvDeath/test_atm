"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from atm import views

urlpatterns = [
    url(r'^$', views.card_number, name='card_number'),
    url(r'^pin/$', views.pin_code, name='pin'),
    url(r'^operations/$', views.operations, name='operations'),
    url(r'^balance/$', views.balance, name='balance'),
    url(r'^withdrawal/$', views.withdrawal, name='withdrawal'),
    url(r'^report/$', views.report, name='report'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^error/$', views.error, name='error'),
    url(r'^admin/', admin.site.urls),
]
