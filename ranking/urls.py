from django.contrib import admin
from django.urls import path
from . import views

app_name = 'ranking'

urlpatterns = [
    # .../ranking/
    path('', views.index, name='index'),
    path('prev/', views.prev_index, name='prev_index')
]