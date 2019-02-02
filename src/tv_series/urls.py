"""tv_series URL Configuration

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

from tv_series import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('add/', views.add_tv_series, name="add_tv_series"),
    path('new', views.new_tv_series, name="new_tv_series"),
    path('<int:tv_series_id>/', views.view_tv_series, name='view_tv_series'),
    path('<str:tv_series_name_year>/', views.view_tv_series_name_year, name='view_tv_series_name_year'),
    path('all/update', views.update_all_tv_series, name='update_all_tv_series'),
]