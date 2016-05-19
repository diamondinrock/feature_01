from django.contrib import admin

from .models import *

admin.site.register(DirPersonnel)
admin.site.register(DirEducationHistory)
admin.site.register(DirEmploymentHistory)
admin.site.register(DirTeam)
admin.site.register(DirTeamMember)
admin.site.register(DirTask)
admin.site.register(DirTaskAssignment)