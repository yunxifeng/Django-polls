from django.conf.urls import url
from . import views

app_name = 'polls'
# polls应用的命名空间
urlpatterns = [
    # url(r'^$', views.index, name="index"),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name="detail"),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name="results"),
    # -改用通用视图后改动如下----------------------------------------------------------------------------
    url(r'^$', views.IndexView.as_view(), name='index'),
    # DetailView希望从url中捕获名为'pk'的主键值
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),

    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name="vote"),
]
