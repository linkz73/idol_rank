from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Ranking
from django.db.models import Q
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_app.views import LoginRequiredMixin


class RankingLV(ListView):
    model = Ranking
    template_name = 'ranking/chart_rank.html'  # 템플릿 이름을 수동으로 설정
    paginate_by = 2  # 한페이지에 2줄
    context_object_name = 'posts'  # 메타에서 사용. tamplates 에서 이름 사용 / object list 대신 사용 가능

