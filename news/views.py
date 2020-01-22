from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import News
from django.db.models import Q
from django.shortcuts import render
from django.forms.models import model_to_dict
from web_crawl.Navernews import *
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
    label_list = ['ab','cd','de','aaa']

    context = {'label_list': label_list}
    # context = {'latest_list': latest_list}
    return render(request, 'news/index.html', context)

def result(request):
    page_info_list = []
    url_list = []
    title_list = []
    news_content_list = []
    content_summarize_list = []
    img_url= []
    value = []
    keyword = request.POST['keyword']
    print("검색어 : ", keyword)
    call_and_print(keyword, 1, page_info_list)
    for i in range(len(page_info_list)):
        url_list.append(page_info_list[i][1])
    make_content(url_list, news_content_list, content_summarize_list, title_list)
    wordcloud(news_content_list, page_info_list, img_url)
    for i in range(len(title_list)):
        values = (title_list[i], url_list[i], img_url[i], content_summarize_list[i])
        value.append(values)
    context = {'keyword': keyword, 'values': value}
    return render(request, 'news/result.html', context)

    '''
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    '''