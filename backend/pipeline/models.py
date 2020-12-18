'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models


TASK_STATUS = (('wait', 'Wait'), ('inprogress', 'Inprogress'), ('error', 'Error'), ('complete', 'Complete'))


class TaskQueue(models.Model):
    experiment_id = models.IntegerField(db_index=True)
    pid = models.IntegerField(db_index=True, default=0)
    status = models.CharField(choices=TASK_STATUS, max_length=20, default='wait')
    cmd = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

