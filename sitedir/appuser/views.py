from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


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
		'tasks_list': [
			{'task_name': 'I am a task', 'task_description': 'I am a task description', 'task_leader': 'Bernie Sanders', 'creation_date': '2016-01-01'},
			{'task_name': 'I am also a task', 'task_description': 'I am also a task description', 'task_leader': 'Barack Obama', 'creation_date': '2016-01-02'},
			{'task_name': 'I am the third task', 'task_description': 'I am the third task description', 'task_leader': 'Hilary Clinton', 'creation_date': '2016-01-03'}
		]
	}

	return render(request, 'appuser/index.html', context)
