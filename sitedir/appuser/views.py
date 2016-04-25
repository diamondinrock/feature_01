from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from .models import DirPersonnel
from . import connector
import json
from . import wechatuser

def index(request):
	# context = {
	# 	'teams_list': Teams.objects.all(), 
	# 	'tasks_list': Tasks.objects.all()
	# }
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
        urlopenid = datadict['openid']
        try:
            person = DirPersonnel.objects.get(openID=urlopenid)
            person_id = person.person_id
            request.session['person_id'] = person_id
            request.session.set_expiry(0)
            request.session.save()
        except DirPersonnel.DoesNotExist:
            pass
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

    
def setpersonid(request, personid):
    request.session['person_id'] = personid
    request.session.set_expiry(0)
    request.session.save()
    context = { 'personid':request.session['person_id'] }
    return render(request, 'appuser/setpersonid.html',context)

def getpersonid(request):
    if 'person_id' in request.session:
        context = { 'personid':request.session['person_id'] }
    else:
        context = { 'personid':'No user set' }
    return render(request, 'appuser/getpersonid.html',context)
    