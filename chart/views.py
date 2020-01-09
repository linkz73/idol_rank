from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Chart, Idol
from django.db.models import Q
from django.shortcuts import render
from django.forms.models import model_to_dict

from django.http import HttpResponse
from django.template import loader

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_app.views import LoginRequiredMixin

from collections import OrderedDict  # dictionary 객체를 render 로 전달하기 위함
import pdb  # 디버깅 용

# def index(request):
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     template = loader.get_template('chart/chart.html')
#     context = {
#         'latest_list': latest_list,
#     }
#     return HttpResponse(template.render(context, request))

# select_related 는 INNER JOIN 으로 쿼리셋을 가져온다.
# prefetch_related 는 모델별로 쿼리를 실행해 쿼리셋을 가져온다.
# 이 모든건 qeryset들이 캐싱되기 때문에 가능

def index(request):    
    # latest_list = Chart.objects.order_by('-chart_id').all()
    # temp_list = Chart.objects.all()
    start_date = '201801'
    
    # print("start date is2 ",start_date)
    # pdb.set_trace()  # 디버깅. 

    ord_dict = OrderedDict()
    ord_dict['2015-06-20'] = {}
    ord_dict['2015-06-20']['a'] = '1'
    ord_dict['2015-06-20']['b'] = '2'
    ord_dict['2015-06-21'] = {}
    ord_dict['2015-06-21']['a'] = '10'
    ord_dict['2015-06-21']['b'] = '20'

    latest_list = Chart.objects.select_related('idol').order_by('chart_date') #foreignkey 변수 이름
    for item in latest_list:
        print(item.idol.idol_name)
    context = {'latest_list': latest_list, 'ord_dict':ord_dict}
    return render(request, 'chart/index.html', context)

# class ChartTV(TemplateView):
#     model = Chart
    
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     latest_list = "aa"

#     template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정

