from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userinfo', views.wechat, name='wechat'),
    url(r'allteams', views.allteams, name='allteams'),
    url(r'alltasks', views.alltasks, name='alltasks'),
    url(r'^team/(?P<teamid>\d+)/$', views.teams),
    url(r'^task/(?P<taskid>\d+)/$', views.taskdetail, name='taskdetail'),
    url(r'^setpersonid/(?P<personid>\d+)/$', views.setpersonid, name='setpersonid'),
    url(r'^getpersonid', views.getpersonid, name='getpersonid'),
]
