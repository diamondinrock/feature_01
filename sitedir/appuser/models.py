# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DirEducationHistory(models.Model):
    person = models.ForeignKey('DirPersonnel', models.DO_NOTHING)
    college_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    major = models.CharField(max_length=45)
    end_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Education_History'
        unique_together = (('college_name', 'start_date', 'person'),)


class DirEmploymentHistory(models.Model):
    person = models.ForeignKey('DirPersonnel', models.DO_NOTHING)
    employer_name = models.CharField(max_length=100)
    employment_start_date = models.DateTimeField()
    job_title = models.CharField(max_length=80)
    employment_end_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Employment_History'
        unique_together = (('employer_name', 'employment_start_date', 'person'),)


class DirPersonnel(models.Model):
    person_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=45)
    openid = models.CharField(db_column='openID', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    province_state = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    goal = models.CharField(max_length=200, blank=True, null=True)
    executive_team_memeber = models.CharField(max_length=10, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DIR_Personnel'


class DirPositions(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=45)
    position_description = models.CharField(max_length=100)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Positions'


class DirTaskAssignments(models.Model):
    person = models.ForeignKey(DirPersonnel, models.DO_NOTHING)
    task = models.ForeignKey('DirTasks', models.DO_NOTHING)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Task_Assignments'
        unique_together = (('task', 'person'),)


class DirTasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=80)
    task_leader = models.CharField(max_length=45)
    task_description = models.CharField(max_length=250)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Tasks'


class DirTeamPositions(models.Model):
    team = models.ForeignKey('DirTeams', models.DO_NOTHING)
    position = models.ForeignKey(DirPositions, models.DO_NOTHING)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Team_Positions'
        unique_together = (('position', 'team'),)


class DirTeams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=80)
    team_description = models.CharField(max_length=100)
    creation_date = models.DateTimeField()
    modifed_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'DIR_Teams'
