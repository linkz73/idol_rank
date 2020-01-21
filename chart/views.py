from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Chart, Idol, Predict
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

# select_related 는 INNER JOIN 으로 쿼리셋을 가져옴
# prefetch_related 는 모델별로 쿼리를 실행해 쿼리셋을 가져옴
# qeryset들이 캐싱되기 때문에 가능

def index(request):    
    # latest_list = Chart.objects.order_by('-chart_id').all()
    start_date = 201801
    start_datef = datetime.datetime.strptime(str(start_date), "%Y%m")
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
        if temp_date > recent_date + relativedelta(months=1):
            break

    top10_idol = Chart.objects.select_related('idol').filter(chart_date=int(recent_date_n)).order_by('-chart_total')[:10]  # 테이블 조인해서 chart_date 로 where 
    i = 0
    label_list = []
    for idi in top10_idol:
        total_list = []
        label_list.append(idi.idol.idol_name)
        # temp_list = Chart.objects.select_related('idol').filter(idol_id=int(idi.idol_id)).order_by('chart_date')
        for date_index in date_list:
            try:
                if int(date_index) == 202001:
                    temp_total = Predict.objects.select_related('idol').filter(idol_id=int(idi.idol_id)).values()[0]['predict_total']
                else:
                    temp_total = Chart.objects.select_related('idol').filter(idol_id=int(idi.idol_id), chart_date=int(date_index)).values()[0]['chart_total']
            except:
                temp_total = 0
            if temp_total is None:
                temp_total = 0
            total_list.append(temp_total)

           
        ord_dict[i] = {}
        ord_dict[i]['name'] = idi.idol.idol_name
        ord_dict[i]['total'] = total_list
        i += 1
    
    month_list = []
    for i in date_list:
        labelMonth = i[0:4] + "년 " + i[4:6] + "월"
        month_list.append(labelMonth)

    # latest_list = Chart.objects.select_related('idol').order_by('chart_date') #foreignkey 변수 이름
    
    context = {'month_list': month_list, 'label_list': label_list, 'ord_dict':ord_dict}
    return render(request, 'chart/index.html', context)

# class ChartTV(TemplateView):
#     model = Chart
    
#     latest_list = Chart.objects.order_by('-chart_id')[:5]
#     latest_list = "aa"

#     template_name = 'chart/chart.html'  # 템플릿 이름을 수동으로 설정

