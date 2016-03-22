import json
from django.http import HttpResponse
from django.core import serializers
from .models import DirTeams#change depending on what models will be
from .models import DirTasks 
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

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
    DirTasks_as_json = serializers.serialize('json', DirTasks.objects.order_by('-creation_date'))
    return DirTasks_as_json
