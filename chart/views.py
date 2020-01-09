from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Chart
from django.db.models import Q
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_app.views import LoginRequiredMixin

# def index(request):
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     template = loader.get_template('chart/chart.html')
#     context = {
#         'latest_list': latest_list,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):    
    # latest_list = Chart.objects.order_by('-chart_id').all()
    latest_list = Chart.objects.all()
    context = {'latest_list': latest_list}
    return render(request, 'chart/index.html', context)

# class ChartTV(TemplateView):
#     model = Chart
    
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     latest_list = "aa"

#     template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정

