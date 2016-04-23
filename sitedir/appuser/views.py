from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from . import connector
import json
from . import wechatuser

def index(request):
	context = {
		'teams_list': [connector.getHotGroups(4)],
		'tasks_list': [connector.getRecentTasks(5)],
	}
	return render(request, 'appuser/index.html', context)

def wechat(request):
    """Renders the wechat page."""
    assert isinstance(request, HttpRequest)
    nsukey = request.GET.get('nsukey', 'none')
    if ( nsukey == 'none'):
        datadict = wechatuser.getUser(request)
    return index(request)

def allteams(request):
	context = { 'teamsjson':[connector.getAllTeams()] }
	return render(request, 'appuser/allteams.html',context)
    
def alltasks(request):
	context = { 'tasksjson':[connector.getAllTasks()] }
	return render(request, 'appuser/task-list.html',context)

def teams(request,teamid):
	context = {'teamjson':[connector.getTeambyID(teamid)]}
	return render(request, 'appuser/team.html',context)

def taskdetail(request, taskid):
    context = {'taskdetail':connector.getTaskbyID(taskid)}
    return render(request, 'appuser/task-detail.html',context)
