import json
from django.http import HttpResponse
from django.core import serializers
from models #change depending on what models will be
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

