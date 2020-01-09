from django.contrib import admin
from django.urls import path
from . import views
# from .views import *

app_name = 'chart'

urlpatterns = [
    # .../chart/
    path('', views.index, name='index'),
    # path('', ChartTV.as_view(), name='index'),
]