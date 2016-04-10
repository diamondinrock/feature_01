from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userinfo', views.wechat, name='wechat'),
    url(r'allteams', views.allteams, name='allteams'),
    url(r'^team/(?P<teamid>\w{0,50})/$', views.teams),
    url(r'^task/(?P<taskid>\d+)/$', views.taskdetail, name='taskdetail'),
]
