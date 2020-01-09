from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Ranking
from django.db.models import Q
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_app.views import LoginRequiredMixin


# class RankingLV(ListView):
#     model = Ranking
#     template_name = 'ranking/chart_rank.html'  # 템플릿 이름을 수동으로 설정
#     paginate_by = 2  # 한페이지에 2줄
#     context_object_name = 'posts'  # 메타에서 사용. tamplates 에서 이름 사용 / object list 대신 사용 가능


def index(request):    
    ranking_list = Chart.objects.select_related('idol').filter(chart_date=int(recent_date_n)).order_by('-chart_total')[:10]  # 테이블 조인해서 chart_date 로 where 
    context = {'ranking_list': ranking_list}
    return render(request, 'chart/index.html', context)

# class ChartTV(TemplateView):
#     model = Chart
    
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     latest_list = "aa"

#     template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정