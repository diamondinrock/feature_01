import json
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeams#change depending on what models will be
from .models import DirTasks 
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
    cursor.execute("select a.team_name, count(distinct(b.task_id)) from dir_teams a, dir_task_assignments b, dir_tasks c where a.team_id = b.team_id and c.task_id = b.task_id and DATEDIFF (c.signup_due_date,NOW()) > 1 group by b.team_id") #executes the sql quere
    numMemberTasks = cursor.fetchone()
    numMemberTasks_as_json = serializers.serialize('json', numMemberTasks.objects.all()) #must test - see if json will take sql results
    return numMemberTasks
    
def getNumNewTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select %s.team_name, count(distinct(%s.task_id)) from dir_teams %s, dir_task_assignments %s where a.team_id = %s.team_id and DATEDIFF (NOW(), %s.modified_date)) < 7 group by %s.team_id", a,b,a,b,a,b,b,b) #executes the sql quere
    numNewTasks = cursor.fetchall()
    numNewTasks_as_json = serializers.serialize('json', numNewTasks.objects.all()) 
    return numNewTasks
    
def getTotalTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select a.team_name, count(distinct(b.task_id)) from dir_teams a, dir_task_assignments b where a.team_id = b.team_id group by b.team_id") #executes the sql quere
    totalTasks = cursor.fetchall()
    totalTasks_as_json = serializers.serialize('json', totalTasks.objects.all()) 
    return totalTasks

def getTeamMembers(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select c.team_name, a.last_name, a.first_name from diamondrough.dir_personnel a, diamondrough.dir_person_position_assignments b, diamondrough.dir_teams c where a.person_id = b.person_id and b.team_id = c.team_id") #executes the sql query, must find out selecting team name parameter
    teamMembers = cursor.fetchall()
    teamMembers_as_json = serializers.serialize('json', teamMembers.objects.all()) #may not need json
    return teamMembers

def getNamesTasks(request):
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select a.team_name, c.task_name from dir_teams a, dir_task_assignments b, dir_tasks c where a.team_id = b.team_id and c.task_id = b.task_id") #executes the sql quere
    namesTasks = cursor.fetchall()
    namesTasks_as_json = serializers.serialize('json', namesTasks.objects.all()) #may not need json
    return namesTasks
    
