from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'chart'

urlpatterns = [
    # .../chart/
    path('', ChartTV.as_view(), name='index'),
]