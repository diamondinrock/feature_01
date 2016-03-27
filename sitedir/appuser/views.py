from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from . import connector
import json
from . import wechatuser

def index(request):
	# context = {
	# 	'teams_list': Teams.objects.all(), 
	# 	'tasks_list': Tasks.objects.all()
	# }
	context = {
		'teams_list': [
			{'team_name':'Production', 'first_letter':'P'},
			{'team_name':'Engineering', 'first_letter':'E'},
			{'team_name':'Transportation', 'first_letter':'T'},
			{'team_name':'Marketing', 'first_letter':'M'}
		],
		'tasks_list': connector.getRecentTasks(request, 5),
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
	context = {'teamsjson':[json.loads(connector.getAllTeams(request))]}
	return render(request, 'appuser/allteams.html',context)
