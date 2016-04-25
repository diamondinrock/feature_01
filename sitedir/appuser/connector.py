import json
import datetime
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeam
from .models import DirTask
from .models import DirPersonnel
from .models import DirTeamMember
from .models import DirEmploymentHistory
from .models import DirEducationHistory
from .models import DirTaskAssignment 
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection 

class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, DirTeams): #models could be something different
            return force_text(obj)
        return super(JSONEncoder, self).default(obj)

def getAllTasks():
    tasks = []
    task_ids = [task.task_id for task in DirTask.objects.all()]
    for task_id in task_ids:
        tasks.append(getTask(task_id))
    return tasks

def getAllTeams():
    '''
    DirTeam_as_json = serializers.serialize('json', DirTeam.objects.all())
    return DirTeam_as_json
    '''
    teams = []
    team_ids = [team.team_id for team in DirTeam.objects.all()]
    for team_id in team_ids:
        teams.append(getTeam(team_id))
    return teams

def getTask(task_id):
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
        taskdetails['task_leader'] = DirPersonnel.objects.get(pk=task.task_leader_id).user_name
    else:
        taskdetails['task_leader'] = 'No leader'
    taskdetails['task_description'] = task.task_description
    taskdetails['signup_due_date'] = task.signup_due_date
    taskdetails['creation_date'] = task.creation_date
    taskdetails['modified_date'] = task.modified_date
    return taskdetails

def getRecentTasks(number_of_tasks):
    task_ids = [ task.task_id for task in DirTask.objects.order_by('-creation_date')[:number_of_tasks] ]
    recenttasks = []
    for task_id in task_ids:
        recenttasks.append(getTask(task_id))
    return recenttasks

def getTeam(team_id):
    team = DirTeam.objects.get(pk=team_id)
    teamdetails = {}
    teamdetails['team_id'] = team.team_id
    teamdetails['team_name'] = team.team_name
    teamdetails['first_letter'] = team.team_name[0]
    if team.team_leader_id is not None:
        teamdetails['team_leader'] = DirPersonnel.objects.get(pk=team.team_leader_id).user_name
    else:
        teamdetails['team_leader'] = 'No leader'
    teamdetails['team_description'] = team.team_description
    teamdetails['number_of_members'] = len(getMemberList(team_id))
    teamdetails['creation_date'] = team.creation_date
    teamdetails['modified_date'] = team.modified_date
    return teamdetails

def getMemberList(team_id):
    members = []
    for member in DirTeamMember.objects.all():
        if member.team_id == team_id:
            members.append(member.person_id)
    return members

def getHotGroups(number_of_groups):
    membercount = {}
    for team in DirTeam.objects.all():
        membercount[team.team_id] = len(getMemberList(team.team_id))
    hotgroupids = list(reversed(sorted(membercount, key=membercount.get)))
    hotgroups = []
    for team_id in hotgroupids[:number_of_groups]:
        hotgroups.append(getTeam(team_id))
    return hotgroups
    

def getTeambyID(teamID):
    teamdetail={}

    #Get team information

    try:
        team = DirTeam.objects.get(pk=teamID)
        teamdetail['team_name']=team.team_name
        teamdetail['team_description']=team.team_description
    except DirTeam.DoesNotExist:
        return teamdetail
    
    #Get team leader

    try:
        leader = DirPersonnel.objects.get(dirteam__team_id__exact=teamID)
        teamdetail['team_leader']=leader.user_name
    except DirPersonnel.DoesNotExist:
        teamdetail['team_leader']= 'No Leader'

    #Get team members
    
    members=[]
    teammembers = DirPersonnel.objects.filter(dirteammember__team_id__exact=teamID)
    for user in teammembers:
        members.append(user.user_name)
    teamdetail['team_members']=members
   
   #Get number of team members
    
    try:
        nummembers = DirPersonnel.objects.filter(dirteammember__team_id__exact=teamID).count()
        teamdetail['num_team_members']=nummembers
    except DirPersonnel.DoesNotExist:
        teamdetail['num_team_members'] = 0

    #Get number of tasks

    try:
        numtask = DirTask.objects.filter(team_id=teamID).count()
        teamdetail['num_total_tasks']=numtask
    except DirTask.DoesNotExist:
        teamdetail['num_total_tasks'] = 0
    try:
        numnewtask = DirTask.objects.filter(team_id=teamID, signup_due_date__gt=datetime.date.today()).count()
        teamdetail['num_new_tasks']=numnewtask
    except DirTask.DoesNotExist:
        teamdetail['num_new_tasks'] = 0

    #Get task names
    
    tasknames = DirTask.objects.filter(team_id=teamID)
    tasks=[]
    for task in tasknames:
        tasks.append([task.task_id, task.task_name])
    teamdetail['team_tasks']=tasks
    
    return teamdetail
    
def getTaskbyID(taskID):
    taskdetail={}
    
    #Get task information
    
    try:
        task = DirTask.objects.get(pk=taskID)
        taskdetail['task_name']=task.task_name
        taskdetail['task_description']=task.task_description
        taskdetail['creation_date']=task.creation_date
        taskdetail['signup_due_date']=task.signup_due_date
    except DirTask.DoesNotExist:
        return taskdetail
        
    #Get team information
    
    try:
        team = DirTeam.objects.get(dirtask__task_id__exact=taskID)
        taskdetail['team_name']=team.team_name
    except DirTeam.DoesNotExist:
        taskdetail['team_name']= 'No Team'
        
    #Get task leader
    
    try:
        leader = DirPersonnel.objects.get(dirtask__task_id__exact=taskID)
        taskdetail['task_leader']=leader.user_name
    except DirPersonnel.DoesNotExist:
        taskdetail['task_leader']= 'No Task Leader'
        
    #Get task members
    
    taskassignment = DirPersonnel.objects.filter(dirtaskassignment__task_id__exact=taskID)
    members=[]
    for user in taskassignment:
        members.append(user.user_name)
    taskdetail['members']=members
    
    return taskdetail

def getPersonalProfile(personID):
    personalprofile={}
    #get firstname, lastname, city, occupation from DirPersonnel 
    try:
        person = DirPersonnel.objects.get(pk=personID)
        personalprofile['first_name']=person.first_name
        personalprofle['last_name']=person.last_name
        personalprofile['team_position']= None
        personalprofile['city']=person.city
        personalprofile['occupation']=person.occupation
    except DirPersonnel.DoesNotExist:
        return personalprofile
    #get college name, major, college start/end date from DirEducationHistory
    try:
        person = DirEducationHistory.objects.get(DirPersonnel__person_id__exact=personID)
        personalprofile['college_name']=person.college_name #note: check if multiple entries of college exist
        personalprofile['major']=person.major
        personalprofile['college_start_date']=person.college_start_date
        personalprofile['college_end_date']=person.college_end_date
    except DirEducationHistory.DoesNotExist:
        return personalprofile #tentative
    #get tasks id from person id

    try:
        person = DirTeamMember.objects.get(DirPersonnel__person_id__exact=personID)
        teamID = person.team_id
        teamid = DirTeam.objects.get(DirTeamMember__team_id_exact=teamID) # may give multiple
        personalprofile['team_name']= teamid.team_name
        
    except DirTeamMember.DoesNotExist:
        return personalprofile

   #tasks number (?) get task id(s)
    try:
        totalTasks = DirTask.objects.filter(person_id=personID).count()
        personalprofile['num_total_tasks']=totalTasks
    except DirTask.DoesNotExist:
        personalprofile['num_total_tasks'] = 0
    try:
        newTasks = DirTask.objects.filter(person_id=personID)
        personalprofile['new_tasks']=newTasks
    except DirTask.DoesNotExist:
        personalprofile
    try:
        completedTasks = DirTask.objects.filter(person_id=personID, completion_date__gt = datetime.date(year=year,month=month,day=day,hour=hour)
        personalprofile['completed_tasks'] = completedTasks
    except DirTask.DoesNotExist:
        personalprofile['completed_tasks'] = None
        
   
             
        
