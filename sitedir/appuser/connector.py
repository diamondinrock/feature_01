import json
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeam#change depending sql
from .models import DirTask
from .models import DirTeamMember
from .models import DirTaskAssignment #possibly incorrect names, must check
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection 

class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, DirTeams): #models could be something different
            return force_text(obj)
        return super(JSONEncoder, self).default(obj)
            
def getAllTeams(request):
    DirTeams_as_json = serializers.serialize('json', DirTeams.objects.all())
    return DirTeams_as_json

def getTask(request, number):
    pk = 'task_id'
    DirTasks_as_json = serializers.serialize('json', DirTasks.objects.filter(pk = number), fields=('task_name', 'task_description', 'task_leader', 'task_description'))
    return DirTasks_as_json

def getRecentTasks(request, number_of_tasks):
    return DirTasks.objects.order_by('-creation_date')[:number_of_tasks] # does not translate into json? cihstliu changed this
    
def getNumMemberTasks(request): #b = task_id number #other variable parameters must check on
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select  a.team_id, b.team_name, a.task_id, a.task_name, count(c.person_id) from diamondrough.dir_task a, diamondrough.dir_team b, diamondrough.dir_task_assignment c where a.team_id = b.team_id and c.task_id = c.task_id group by b.team_id, a.task_id") #executes the sql quere
    numMemberTasks = cursor.fetchone()
    numMemberTasks_as_json = serializers.serialize('json', numMemberTasks.objects.all()) #must test - see if json will take sql results
    return numMemberTasks
    
def getNumNewTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select a.team_id, a.team_name, count(distinct(b.task_id)) from dir_team a, dir_task b where a.team_id = b.team_id and DATEDIFF (b.signup_due_date,NOW()) > 1 group by b.team_id") #executes the sql 
    numNewTasks = cursor.fetchall()
    numNewTasks_as_json = serializers.serialize('json', numNewTasks.objects.all()) 
    return numNewTasks
    
def getTotalTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select  a.team_id, b.team_name, count(a.task_id) from diamondrough.dir_task a, diamondrough.dir_team b where a.team_id = b.team_id group by b.team_id") #executes the sql 
    totalTasks = cursor.fetchall()
    totalTasks_as_json = serializers.serialize('json', totalTasks.objects.all()) 
    return totalTasks

def getTeamMembers(request): #need team parameter
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select c.team_id, c.team_name, a.last_name, a.first_name from diamondrough.dir_personnel a, diamondrough.dir_team_member b,  diamondrough.dir_team c where a.person_id = b.person_id  and b.team_id = c.team_id") #executes the sql query, must find out selecting team name parameter
    teamMembers = cursor.fetchall()
    teamMembers_as_json = serializers.serialize('json', teamMembers.objects.all()) #may not need json
    return teamMembers

def getNamesTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select a.team_id, a.team_name, b.task_name from dir_team a,   dir_task b where a.team_id = b.team_id") #executes the sql 
    namesTasks = cursor.fetchall()
    namesTasks_as_json = serializers.serialize('json', namesTasks.objects.all()) #may not need json
    return namesTasks
    
