from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'chart'

urlpatterns = [
    # .../blog/
    path('', PostLV.as_view(), name='index'),
    # .../blog/post/
    path('chart/', PostLV.as_view(), name='post_list'),
    # .../blog/post/slug
    # path('post/<str:slug>/', PostDV.as_view(), name='post_detail'),
    
]