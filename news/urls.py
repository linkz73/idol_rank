from django.contrib import admin
from django.urls import path
from . import views
# from .views import *

app_name = 'news'

urlpatterns = [
    # .../chart/
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    # path('', ChartTV.as_view(), name='index'),
]