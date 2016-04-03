import json
import datetime
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeam#change depending sql
from .models import DirTask
from .models import DirPersonnel
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
    DirTeam_as_json = serializers.serialize('json', DirTeam.objects.all())
    return DirTeams_as_json

def getTask(request, task_id):
    '''
    pk = 'task_id'
    DirTask_as_json = serializers.serialize('json', DirTask.objects.filter(pk = number), fields=('task_name', 'task_description', 'task_leader', 'task_description'))
    return DirTask_as_json
    '''
    task = DirTask.objects.get(pk=task_id)
    taskdetails = {}
    taskdetails['task_id'] = task.task_id
    taskdetails['team_name'] = DirTeam.objects.get(pk=task.team_id).team_name
    taskdetails['task_name'] = task.task_name
    if task.task_leader_id is not None:
        taskdetails['task_leader_user_name'] = DirPersonnel.objects.get(pk=task.task_leader_id).user_name
    else:
        taskdetails['task_leader_user_name'] = 'No leader'
    taskdetails['task_description'] = task.task_description
    taskdetails['signup_due_date'] = task.signup_due_date
    taskdetails['creation_date'] = task.creation_date
    taskdetails['modified_date'] = task.modified_date
    return taskdetails

def getRecentTasks(request, number_of_tasks):
    taskidlist = [task.task_id for task in DirTask.objects.order_by('-creation_date')[:number_of_tasks]]
    recenttasks = []
    for task_id in taskidlist:
        recenttasks.append(getTask(request, task_id))
    return recenttasks

def getTeam(request, team_id):
    team = DirTeam.objects.get(pk=team_id)
    teamdetails = {}
    teamdetails['team_id'] = team.team_id
    teamdetails['team_name'] = team.team_name
    teamdetails['first_letter'] = team.team_name[0]
    if team.team_leader_id is not None:
        teamdetails['team_leader_user_name'] = DirPersonnel.objects.get(pk=team.team_leader_id).user_name
    else:
        teamdetails['team_leader_user_name'] = 'No leader'
    teamdetails['team_description'] = team.team_description
    teamdetails['creation_date'] = team.creation_date
    teamdetails['modified_date'] = team.modified_date
    return teamdetails

def getMemberList(request, team_id):
    members = []
    for member in DirTeamMember.objects.all():
        if member.team_id == team_id:
            members.append(member.person_id)
    return members

def getHotGroups(request, number_of_groups):
    membercount = {}
    for team in DirTeam.objects.all():
        membercount[team.team_id] = len(getMemberList(request, team.team_id))
    hotgroupids = list(reversed(sorted(membercount, key=membercount.get)))
    hotgroups = []
    for team_id in hotgroupids[:number_of_groups]:
        hotgroups.append(getTeam(request, team_id))
    return hotgroups
    
def getNumMemberTasks(request): #b = task_id number #other variable parameters must check on
    cursor = connection.cursor()  #creates cursor
    cursor.execute("select  a.team_id, b.team_name, a.task_id, a.task_name, count(c.person_id) from diamondrough.dir_task a, diamondrough.dir_team b, diamondrough.dir_task_assignment c where a.team_id = b.team_id and c.task_id = c.task_id group by b.team_id, a.task_id") #executes the sql quere
    numMemberTasks = cursor.fetchall()
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
    
def getTeambyID(teamID):
    teamdetail={}
    
    try:
        DirTeamInfo = serializers.serialize('json', DirTeam.objects.filter(pk=teamID), fields=('team_name', 'team_description'))
    except DirTeam.DoesNotExist:
        return teamdetail
    
    try:
        DirTeamLeader = serializers.serialize('json', DirPersonnel.objects.filter(dirteam__team_id__exact=teamID), fields=('user_name'))
    except DirPersonnel.DoesNotExist:
         DirTeamLeader = 'None'    
    
    try:
        DirTeamMembers = serializers.serialize('json', DirPersonnel.objects.filter(dirteammember__team_id__exact=teamID), fields=('user_name'))
        NumDirTeamMembers = DirPersonnel.objects.filter(dirteammember__team_id__exact=teamID).count()
    except DirPersonnel.DoesNotExist:
        NumDirTeamMembers = 0
    
    try:
        DirTeamTasks = serializers.serialize('json', DirTask.objects.filter(team_id=teamID), fields=('task_name'))
        NumDirTeamTasks = DirTask.objects.filter(team_id=teamID).count()
    except DirTask.DoesNotExist:
        NumDirTeamTasks = 0
    
    try:
        DirNewTeamTasks = serializers.serialize('json', DirTask.objects.filter(team_id=teamID, signup_due_date__gt=datetime.date.today()))
        NumDirNewTeamTasks = DirTask.objects.filter(team_id=teamID, signup_due_date__gt=datetime.date.today()).count()
    except DirTask.DoesNotExist:
        NumDirNewTeamTasks = 0
        
    teamdetail['team_name']=json.loads(DirTeamInfo)[0]['fields']['team_name']
    teamdetail['team_leader']=json.loads(DirTeamLeader)[0]['fields']['user_name']
    teamdetail['team_description']=json.loads(DirTeamInfo)[0]['fields']['team_description']
    teamdetail['num_team_members']=NumDirTeamMembers
    teamdetail['num_total_tasks']=NumDirTeamTasks
    teamdetail['num_new_tasks']=NumDirNewTeamTasks
    members=[]
    if (NumDirTeamMembers > 0):
        for user in json.loads(DirTeamMembers):
            members.append(user['fields']['user_name'])
    teamdetail['team_members']=members
    tasks=[]
    if (NumDirTeamTasks > 0):
        for task in json.loads(DirTeamTasks):
            tasks.append(task['fields']['task_name'])
    teamdetail['team_tasks']=tasks
    return teamdetail
    
def getTaskbyID(taskID):
    DirPeopleInTask = serializers.serialize('json', DirPersonnel.objects.filter(dirtaskassignment__task_id__exact=taskID), fields=('user_name'))
    DirLeaderInfo = serializers.serialize('json', DirPersonnel.objects.filter(dirtask__task_id__exact=taskID), fields=('user_name'))
    DirTeamInfo = serializers.serialize('json', DirTeam.objects.filter(dirtask__task_id__exact=taskID), fields=('team_name'))
    DirTaskInfo = serializers.serialize('json', DirTask.objects.filter(pk=taskID), fields=('task_name', 'task_description', 'creation_date', 'signup_due_date'))
    taskdetail={}
    taskdetail['team_name']=json.loads(DirTeamInfo)[0]['fields']['team_name']
    taskdetail['team_leader']=json.loads(DirLeaderInfo)[0]['fields']['user_name']
    taskdetail['task_name']=json.loads(DirTaskInfo)[0]['fields']['task_name']
    taskdetail['task_description']=json.loads(DirTaskInfo)[0]['fields']['task_description']
    taskdetail['creation_date']=json.loads(DirTaskInfo)[0]['fields']['creation_date']
    taskdetail['signup_due_date']=json.loads(DirTaskInfo)[0]['fields']['signup_due_date']
    members=[]
    for user in json.loads(DirPeopleInTask):
        members.append(user['fields']['user_name'])
    taskdetail['members']=members
    return taskdetail

