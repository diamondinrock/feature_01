from django.db import models

# Create your models here.
class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_leader = models.IntegerField(default=0)
    task_description = models.CharField(max_length=500)
    creation_date = models.DateTimeField('Date Created')
    modified_date = models.DateTimeField('Date Modified')

class Personnel(models.Model):
    person_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    openid = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    
