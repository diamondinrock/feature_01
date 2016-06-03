from django.contrib import admin
from django import forms
from .models import *

admin.site.register(DirPersonnel)
admin.site.register(DirEducationHistory)
admin.site.register(DirEmploymentHistory)
admin.site.register(DirTeam)
admin.site.register(DirTask)
admin.site.register(DirTaskAssignment)

class TeamMemberAdmin(admin.ModelAdmin):
    fields = ('person', 'team', 'member_status', 'self_introduction', 'contact_information')
    readonly_fields = ('person', 'team', 'contact_information', 'self_introduction')
    list_filter = ('member_status', 'team_id', 'person_id')

admin.site.register(DirTeamMember, TeamMemberAdmin)
