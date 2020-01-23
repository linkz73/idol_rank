"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from .views import *
# from .views import UserCreateView, UserCreateDoneTV4

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/register/', UserCreateView.as_view(), name='register'),
    # path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('', HomeView.as_view(), name='home'),  # 홈 뷰 추가
    path('chart/', include('chart.urls',), name='chart'),
    path('ranking/', include('ranking.urls',), name='ranking'),
    path('news/', include('news.urls',), name='news'),

    path('description/news', Description_NewsView.as_view(), name='description_news'),
    path('description/chart', Description_ChartView.as_view(), name='description_chart'),
    path('description/data', Description_DataView.as_view(), name='description_data'),
]