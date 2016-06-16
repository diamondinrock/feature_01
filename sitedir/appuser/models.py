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
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=100)
    college_start_date = models.DateField()
    major = models.CharField(max_length=45)
    college_end_date = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return '%s at %s' % (self.person.user_name, self.college_name)

    class Meta:
        managed = False
        db_table = 'dir_education_history'


class DirEmploymentHistory(models.Model):
    person = models.ForeignKey('DirPersonnel', models.DO_NOTHING)
    employer_name = models.CharField(max_length=100)
    employment_start_date = models.DateTimeField()
    job_title = models.CharField(max_length=80)
    employment_end_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return '%s at %s' % (self.person.user_name, self.employer_name)

    class Meta:
        managed = False
        db_table = 'dir_employment_history'


class DirPersonnel(models.Model):
    person_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=45)
    openid = models.CharField(db_column='openID', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    header_url = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    middle_name = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=45)
    province_state = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    occupation = models.CharField(max_length=45)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    self_introduction = models.CharField(max_length=1000, blank=True, null=True)
    executive_team_member = models.CharField(max_length=10, blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return self.user_name

    class Meta:
        managed = False
        db_table = 'dir_personnel'


class DirTask(models.Model):
    task_id = models.AutoField(primary_key=True)
    team = models.ForeignKey('DirTeam', models.DO_NOTHING)
    task_name = models.CharField(max_length=80)
    task_leader = models.ForeignKey(DirPersonnel, models.DO_NOTHING, blank=True, null=True)
    task_description = models.CharField(max_length=250)
    signup_due_date = models.DateField()
    completion_date = models.DateField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return 'Task %s: %s under %s' % (self.task_id, self.task_name, self.team.team_name)

    class Meta:
        managed = False
        db_table = 'dir_task'


class DirTaskAssignment(models.Model):
    person = models.ForeignKey(DirPersonnel, models.DO_NOTHING)
    task = models.ForeignKey(DirTask, models.DO_NOTHING)
    comments = models.CharField(max_length=100, blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return 'Task %s assigned to %s' % (self.task.task_id, self.person.user_name)

    class Meta:
        managed = False
        db_table = 'dir_task_assignment'


class DirTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=80)
    team_leader = models.ForeignKey(DirPersonnel, models.DO_NOTHING, blank=True, null=True)
    team_description = models.CharField(max_length=100)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return self.team_name

    class Meta:
        managed = False
        db_table = 'dir_team'


class DirTeamMember(models.Model):
    person = models.ForeignKey(DirPersonnel, models.DO_NOTHING)
    team = models.ForeignKey(DirTeam, models.DO_NOTHING)
    MEMBER_STATUS_CHOICES = (
        ('Accept', 'Accepted'),
        ('Reject', 'Rejected'),
        ('Pending', 'Pending'),
    )
    member_status = models.CharField(max_length=45,choices=MEMBER_STATUS_CHOICES, default='Pending')
    contact_information = models.CharField(max_length=80, blank=True, null=True)
    self_introduction = models.CharField(max_length=1000, blank=True, null=True)
    creation_date = models.DateTimeField()
    modified_date = models.DateTimeField()

    def __str__(self):
        return '%s is a member of %s' % (self.person.user_name, self.team.team_name)

    class Meta:
        managed = False
        db_table = 'dir_team_member'
