from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Chart
from django.db.models import Q
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from website.views import LoginRequiredMixin


class ChartTV(TemplateView):
    model = Chart
    template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정

