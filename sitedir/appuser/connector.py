import json
import datetime
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeam#change depending sql
from .models import DirTask
from .models import DirPersonnel
from .models import DirTeamMember
from .models import DirTaskAssignment #possibly incorrect names, must check
from .models import DirEmploymentHistory
from .models import DirEducationHistory
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
    teams = []
    team_ids = [team.team_id for team in DirTeam.objects.all()]
    for team_id in team_ids:
        teams.append(getTeam(team_id))
    return teams

def getTask(task_id):
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

def getPersonnelData(person_id):
    personnel = DirPersonnel.objects.get(pk=person_id)
    data = {}
    data['user_name'] = personnel.user_name
    data['first_name'] = personnel.first_name
    data['last_name'] = personnel.last_name
    data['name'] = data['first_name'] + ' ' + data['last_name']
    data['city'] = personnel.city
    data['occupation'] = personnel.occupation
    data['creation_date'] = personnel.creation_date
    data['modified_date'] = personnel.modified_date
    
    openid = personnel.openid
    if openid is None:
        openid = ''
    data['openid'] = openid
    header_url = personnel.header_url
    if header_url is None:
        header_url = ''
    data['header_url'] = header_url
    middle_name = personnel.middle_name
    if middle_name is None:
        middle_name = ''
    data['middle_name'] = middle_name
    gender = personnel.gender
    if gender is None:
        gender = ''
    data['gender'] = gender
    province_state = personnel.province_state
    if province_state is None:
        province_state = ''
    data['province_state'] = province_state
    country = personnel.country
    if country is None:
        country = ''
    data['country'] = country
    email_address = personnel.email_address
    if email_address is None:
        email_address = ''
    data['email_address'] = email_address
    self_introduction = personnel.self_introduction
    if self_introduction is None:
        self_introduction = ''
    data['self_introduction'] = self_introduction
    executive_team_member = personnel.executive_team_member
    if executive_team_member is None:
        executive_team_member = ''
    data['executive_team_member'] = executive_team_member
    
    return data

def updatePersonnelData(person_id, user_name=None, openid=None, header_url=None, first_name=None, middle_name=None, last_name=None, gender=None, city=None, province_state=None, country=None, occupation=None, email_address=None, self_introduction=None, executive_team_member=None):
    personnel = DirPersonnel.objects.get(pk=person_id)
    if user_name:
        personnel.user_name = user_name
    if openid:
        personnel.openid = openid
    if header_url:
        personnel.header_url = header_url
    if first_name:
        personnel.first_name = first_name
    if middle_name:
        personnel.middle_name = middle_name
    if last_name:
        personnel.last_name = last_name
    if gender:
        personnel.gender = gender
    if city:
        personnel.city = city
    if province_state:
        personnel.province_state = province_state
    if country:
        personnel.country = country
    if occupation:
        personnel.occupation = occupation
    if email_address:
        personnel.email_address = email_address
    if self_introduction:
        personnel.self_introduction = self_introduction
    if executive_team_member:
        personnel.executive_team_member = executive_team_member

    try:
        personnel.save()
    except:
        print('Error occured while updating personnel data')
        return -1
    return 1

def addEducationHistory(person_id, college_name, college_start_date, major, college_end_date=None):
    education = DirEducationHistory(person_id=person_id, college_name=college_name, college_start_date=college_start_date, major=major, college_end_date=college_end_date)
    try:
        education.save()
    except:
        print('Error occured while adding education history')
        return -1
    return 1

def removeEducationHistory(person_id, college_name, college_start_date):
    education = DirEducationHistory.objects.filter(person_id=person_id, college_name=college_name, college_start_date=college_start_date)
    if not len(education):
        print('No matching education history')
        return -1
    try:
        education.delete()
    except:
        print('Error occured while deleting education history')
        return -1
    return 1

def addEmploymentHistory(person_id, employer_name, employment_start_date, job_title, employment_end_date=None):
    employment = DirEmploymentHistory(person_id=person_id, employer_name=employer_name, employment_start_date=employment_start_date, job_title=job_title, employment_end_date=employment_end_date)
    try:
        employment.save()
    except:
        print('Error occured while adding employment history')
        return -1
    return 1

def removeEmploymentHistory(person_id, employer_name, employment_start_date):
    employment = DirEmploymentHistory.objects.filter(person_id=person_id).filter(employer_name=employer_name).filter(employment_start_date=employment_start_date)
    if not len(employment):
        print('No matching employment history')
        return -1
    try:
        employment.delete()
    except:
        print('Error occured while deleting employment history')
        return -1
    return 1

def getEducationHistoryByPersonnel(person_id):
    education_history = DirEducationHistory.objects.filter(person_id=person_id)
    data = []
    for education in education_history:
        educationdata = {}
        educationdata['student_name'] = getPersonnelData(person_id)['name']
        educationdata['college_start_date'] = education.college_start_date
        educationdata['major'] = education.major
        educationdata['creation_date'] = education.creation_date
        educationdata['modified_date'] = education.modified_date
        college_end_date = education.college_end_date
        if college_end_date is None:
            college_end_date = ''
        educationdata['college_end_date'] = college_end_date
        data.append(educationdata)

    return data

def getEmploymentHistoryByPersonnel(person_id):
    employment_history = DirEmploymentHistory.objects.filter(person_id=person_id)
    data = []
    for employment in employment_history:
        employmentdata = {}
        employmentdata['employee_name'] = getPersonnelData(person_id)['name']
        employmentdata['employer_name'] = employment.employer_name
        employmentdata['employment_start_date'] = employment.employment_start_date
        employmentdata['creation_date'] = employment.creation_date
        employmentdata['modified_date'] = employment.modified_date
        employment_end_date = employment.employment_end_date
        if employment_end_date is None:
            employment_end_date = ''
        employmentdata['employment_end_date'] = employment_end_date
        data.append(employmentdata)

    return data

# education_history and employment_history are lists of dictionaries
# dictionary are from above 2 functions
def getPersonalProfileSettingsData(person_id):
    data = {}
    personneldata = getPersonnelData(person_id)
    data['name'] = personneldata['name']
    data['city'] = personneldata['city']
    data['education_history'] = getEducationHistoryByPersonnel(person_id)
    data['employment_history'] = getEmploymentHistoryByPersonnel(person_id)

    return data


    
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

