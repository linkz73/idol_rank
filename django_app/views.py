from django.views.generic.base import TemplateView
# base html : 공통 헤더 등
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
# from django.core.urlresolvers import reverse_lazy
# Django 2.0 에서 django.core.urlresolvers 모듈이 삭제됨.
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = 'home.html'


class Description_NewsView(TemplateView):
    template_name = 'description_news.html'

class Description_DataView(TemplateView):
    template_name = 'description_data.html'

class Description_ChartView(TemplateView):
    template_name = 'description_chart.html'


class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')




class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


