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
import datetime
from dateutil.relativedelta import relativedelta

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
    start_date = 201801
    start_datef = datetime.datetime.strptime(str(start_date), "%Y%m")
    # print("start date is2 ",start_date)
    # pdb.set_trace()  # 디버깅. 

    ord_dict = OrderedDict()

    recent_date0 = Chart.objects.order_by('-chart_date').values()[:1]
    recent_date_n = str(recent_date0[0]['chart_date'])
    recent_date = datetime.datetime.strptime(recent_date_n, "%Y%m")
    temp_date = start_datef
    date_list = []

    while True:
        date_list.append(temp_date.strftime("%Y%m"))
        temp_date += relativedelta(months=1)
        if temp_date > recent_date:
            break
    # for i in date_list:
    #     labelMonth = i[0:4] + "년 " + i[4:6] + "월"
    #     label_list.append(labelMonth)

    top10_idol = Chart.objects.select_related('idol').filter(chart_date=int(recent_date_n)).order_by('-chart_total')[:10]  # 테이블 조인해서 chart_date 로 where 
    i = 0
    label_list = []
    for ii in top10_idol:
        total_list = []
        label_list.append(ii.idol.idol_name)
        temp_list = Chart.objects.select_related('idol').filter(idol_id=int(ii.idol_id)).order_by('chart_total')
        for item in temp_list:
            total_list.append(item.chart_total)
        ord_dict[i] = {}
        ord_dict[i]['name'] = ii.idol.idol_name
        ord_dict[i]['total'] = total_list
        i += 1
    
    month_list = []
    for i in date_list:
        labelMonth = i[0:4] + "년 " + i[4:6] + "월"
        month_list.append(labelMonth)
        print(labelMonth)

        # recent_date0 = Chart.objects.select_related('idol').order_by('-chart_date').values()[:1]
        # recent_date = str(recent_date0[0]['chart_date'])
        # recent_date = datetime.datetime.strptime(recent_date, "%Y%m")
        
        # ord_dict['2015-06-20'] = {}
        # ord_dict['2015-06-20']['a'] = '1'
        # ord_dict['2015-06-20']['b'] = '2'
        # ord_dict['2015-06-21'] = {}
        # ord_dict['2015-06-21']['a'] = '10'
        # ord_dict['2015-06-21']['b'] = '20'
    print(month_list)
    # latest_list = Chart.objects.select_related('idol').order_by('chart_date') #foreignkey 변수 이름
    
    context = {'month_list': month_list, 'label_list': label_list, 'ord_dict':ord_dict}
    # context = {'latest_list': latest_list}
    return render(request, 'chart/index.html', context)

# class ChartTV(TemplateView):
#     model = Chart
    
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     latest_list = "aa"

#     template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정

