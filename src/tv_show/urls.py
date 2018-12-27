"""tv_show URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from tv_show import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('add/', views.add_tv_show, name="add_tv_show"),
    path('new', views.new_tv_show, name="new_tv_show"),
    path('<int:tv_show_id>/', views.view_tv_show, name='view_tv_show'),
    path('<str:tv_show_name_year>/', views.view_tv_show_name_year, name='view_tv_show_name_year'),
    path('all/update', views.update_all_tv_shows, name='update_all_tv_shows'),
]