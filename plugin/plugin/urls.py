"""plugin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from editor import views
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('new/', views.new, name='new'),
    path('download/', views.download, name='download'),
    path('about/', views.about, name='about'),
    path('all_text/', views.all_text, name='all_text'),
    path('first_select/', views.first_select, name='first_select'),
    path('second_select/', views.second_select, name='second_select'),
    path('third_select/', views.third_select, name='third_select'),
    path('fourth_select/', views.fourth_select, name='fourth_select'),
    path('fifth_select/', views.fifth_select, name='fifth_select'),
    path('showText/', views.showText, name='showText'),
]
