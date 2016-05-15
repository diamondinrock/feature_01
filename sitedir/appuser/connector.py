import json
import datetime
from django.http import HttpResponse
from django.core import serializers
from .models import *
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
    taskdetails = {}
    try:
        task = DirTask.objects.get(pk=task_id)
    except DirTask.DoesNotExist:
        print('No such task to get details')
        return taskdetails
    
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
    teamdetails = {}
    try:
        team = DirTeam.objects.get(pk=team_id)
    except DirTeam.DoesNotExist:
        print('No such team to get details')
        return teamdetails
    
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
    data = {}
    try:
        personnel = DirPersonnel.objects.get(pk=person_id)
    except DirPersonnel.DoesNotExist:
        print('No such personnel to get data')
        return data
    
    data['user_name'] = personnel.user_name
    data['first_name'] = personnel.first_name
    data['last_name'] = personnel.last_name
    data['name'] = data['first_name'] + ' ' + data['last_name']
    data['city'] = personnel.city
    data['occupation'] = personnel.occupation
    data['creation_date'] = personnel.creation_date
    data['modified_date'] = personnel.modified_date

    attr = ['openid', 'header_url', 'middle_name', 'gender', 'province_state', 'country', 'email_address', 'self_introduction', 'executive_team_member']
    for field in attr:
        value = getattr(personnel, field)
        if value is None:
            value = ''
        data[field] = value
    
    return data

def updatePersonnelData(person_id, new_user_name=None, new_openid=None, new_header_url=None, new_first_name=None, new_middle_name=None, new_last_name=None, new_gender=None, new_city=None, new_province_state=None, new_country=None, new_occupation=None, new_email_address=None, new_self_introduction=None, new_executive_team_member=None):
    try:
        personnel = DirPersonnel.objects.get(pk=person_id)
    except DirPersonnel.DoesNotExist:
        print('No such personnel to update')
        return -1

    fields = ['user_name', 'openid', 'header_url', 'first_name', 'middle_name', 'last_name', 'gender', 'city', 'province_state', 'country', 'occupation', 'email_address', 'self_introduction', 'executive_team_member']
    new_values = [new_user_name, new_openid, new_header_url, new_first_name, new_middle_name, new_last_name, new_gender, new_city, new_province_state, new_country, new_occupation, new_email_address, new_self_introduction, new_executive_team_member]

    for i in range(len(fields)):
        if new_values[i]:
            setattr(personnel, fields[i], new_values[i])

    try:
        personnel.save()
    except:
        print('Error occured while updating personnel data')
        return -1
    return 1

def isMember(person_id, team_id):
    return person_id in getMemberList(team_id)

def addTask(team_id, task_name, task_description, signup_due_date, task_leader_id=None, completion_date=None):
    task = DirTask(team_id=team_id, task_name=task_name, task_leader_id=task_leader_id, task_description=task_description, signup_due_date=signup_due_date, completion_date=completion_date)
    try:
        task.save()
    except:
        print('Error occured while adding task')
        return -1
    return 1

def removeTask(task_id):
    task = DirTask.objects.filter(pk=task_id)
    if not task:
        print('No matching task to remove')
        return 0

    try:
        task.delete()
    except:
        print('Error occured while deleting task')
        return -1
    return 1

def updateTaskData(task_id, new_task_name=None, new_task_leader_id=None, new_task_description=None, new_signup_due_date=None, new_completion_date=None):
    try:
        task = DirTask.objects.get(pk=task_id)
    except DirTask.DoesNotExist:
        print('No such task to update')
        return 0

    if new_task_name:
        task.task_name = new_task_name
    if new_task_leader_id:
        task.task_leader_id = new_task_leader_id
    if new_task_description:
        task.task_description = new_task_description
    if new_signup_due_date:
        task.signup_due_date = new_signup_due_date
    if new_completion_date:
        task.completion_date = new_completion_date

    try:
        task.save()
    except:
        print('Error occured while updating task data')
        return -1
    return 1

def addEducationHistory(person_id, college_name, college_start_date, major, college_end_date=None):
    existing = DirEducationHistory.objects.get(person_id=person_id, college_name=college_name, college_start_date=college_start_date)
    if existing:
        print('This education history already exists')
        return 0
    
    education = DirEducationHistory(person_id=person_id, college_name=college_name, college_start_date=college_start_date, major=major, college_end_date=college_end_date)
    try:
        education.save()
    except:
        print('Error occured while adding education history')
        return -1
    return 1

def removeEducationHistory(person_id, college_name, college_start_date):
    education = DirEducationHistory.objects.filter(person_id=person_id, college_name=college_name, college_start_date=college_start_date)
    if not education:
        print('No matching education history to remove')
        return 0
    
    try:
        education.delete()
    except:
        print('Error occured while deleting education history')
        return -1
    return 1

def updateEducationHistoryData(person_id, college_name, college_start_date, new_college_name=None, new_college_start_date=None, new_major=None, new_college_end_date=None):
    try:
        education = DirEducationHistory.objects.get(person_id=person_id, college_name=college_name, college_start_date=college_start_date)
    except DirEducationHistory.DoesNotExist:
        print('No such education history to update')
        return 0
    except DirEducationHistory.MultipleObjectsReturned:
        print('Error in database, duplicate education histories')
        return -1
    
    if new_college_name:
        education.college_name = new_college_name
    if new_college_start_date:
        education.college_start_date = new_college_start_date
    if new_major:
        education.major = new_major
    if new_college_end_date:
        education.college_end_date = new_college_end_date

    try:
        education.save()
    except:
        print('Error occured while updating education history data')
        return -1
    return 1

def addEmploymentHistory(person_id, employer_name, employment_start_date, job_title, employment_end_date=None):
    existing = DirEmploymentHistory.objects.get(person_id=person_id, employer_name=employer_name, employment_start_date=employment_start_date)
    if existing:
        print('This employment history already exists')
        return 0
    
    employment = DirEmploymentHistory(person_id=person_id, employer_name=employer_name, employment_start_date=employment_start_date, job_title=job_title, employment_end_date=employment_end_date)
    try:
        employment.save()
    except:
        print('Error occured while adding employment history')
        return -1
    return 1

def removeEmploymentHistory(person_id, employer_name, employment_start_date):
    employment = DirEmploymentHistory.objects.filter(person_id=person_id, employer_name=employer_name, employment_start_date=employment_start_date)
    if not employment:
        print('No matching employment history to remove')
        return 0
    
    try:
        employment.delete()
    except:
        print('Error occured while deleting employment history')
        return -1
    return 1

def updateEmploymentHistoryData(person_id, employer_name, employment_start_date, new_employer_name=None, new_employment_start_date=None, new_job_title=None, new_employment_end_date=None):
    try:
        employment = DirEmploymentHistory.objects.get(person_id=person_id, employer_name=employer_name, employment_start_date=employment_start_date)
    except DirEmploymentHistory.DoesNotExist:
        print('No such employment history to update')
        return 0
    except DirEmploymentHistory.MultipleObjectsReturned:
        print('Error in database, duplicate employment histories')
        return -1
    
    if new_employer_name:
        employment.employer_name = new_employer_name
    if new_employment_start_date:
        employment.employment_start_date = new_employment_start_date
    if new_job_title:
        employment.job_title = new_job_title
    if new_employment_end_date:
        employment.employment_end_date = new_employment_end_date

    try:
        employment.save()
    except:
        print('Error occured while updating employment history data')
        return -1
    return 1

def getRecentEducation(person_id):
    data = {}
    educations = getEducationHistoryByPersonnel(person_id)
    if not educations:
        return data
    data = educations[0]
    return data

def getEducationHistoryByPersonnel(person_id):
    data = []
    education_history = DirEducationHistory.objects.filter(person_id=person_id).order_by('-college_start_date')
    if not education_history:
        return data
    
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

def getRecentEmployment(person_id):
    data = {}
    employments = getEmploymentHistoryByPersonnel(person_id)
    if not employments:
        return data
    data = employments[0]
    return data

def getEmploymentHistoryByPersonnel(person_id):
    data = []
    employment_history = DirEmploymentHistory.objects.filter(person_id=person_id).order_by('-employment_start_date')
    if not employment_history:
        return data
    
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
    if not personneldata:
        print('No such personnel to get settings data')
        return data
    
    data['name'] = personneldata['name']
    data['city'] = personneldata['city']
    data['education_history'] = getEducationHistoryByPersonnel(person_id)
    data['employment_history'] = getEmploymentHistoryByPersonnel(person_id)

    return data



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
        personalprofile['last_name']=person.last_name
        personalprofile['team_position']= None
        personalprofile['city']=person.city
        personalprofile['occupation']=person.occupation
        personalprofile['self_introduction'] = person.self_introduction
    except DirPersonnel.DoesNotExist:
        return personalprofile
    try:
        person = DirEmploymentHistory.objects.get(DirPersonnel__person_id__exact=personID)
        personalprofile['company']= person.employer_name #company != employername?
    except DirEmploymentHistory.DoesNotExist:
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
    try:
        totalTasks = DirTask.objects.filter(person_id=personID).count()
        personalprofile['num_total_tasks']=totalTasks
    except DirTask.DoesNotExist:
        personalprofile['num_total_tasks'] = 0
    try:
        newTasks= DirTask.objects.filter(person_id=personID).filter(testfield=12).latest('testfield')
        personalprofile['new_tasks']=newTasks
    except DirTask.DoesNotExist:
        personalprofile
    try:
        completedTasks = DirTask.objects.filter(person_id=personID, completion_date__gt = datetime.date(year=year,month=month,day=day,hour=hour))
        personalprofile['completed_tasks'] = completedTasks
    except DirTask.DoesNotExist:
        personalprofile['completed_tasks'] = None

