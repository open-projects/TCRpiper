'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import psutil
from django.db import models


TASK_STATUS = (('wait', 'Wait'), ('inprogress', 'Inprogress'), ('error', 'Error'), ('complete', 'Complete'))


class TaskQueue(models.Model):
    experiment_id = models.IntegerField(db_index=True)
    thread = models.IntegerField(db_index=True, default=0, unique=True)
    pid = models.IntegerField(db_index=True, default=0)
    cmd = models.CharField(max_length=200)
    status = models.CharField(choices=TASK_STATUS, max_length=20, default='wait')
    date = models.DateTimeField(auto_now_add=True)


def taskRemover():
    n = 0
    for task in TaskQueue.objects.all():
        if not psutil.pid_exists(task.pid):
            task.delete()
            n += 1
    return n




