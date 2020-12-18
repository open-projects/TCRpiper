'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models


class ExecuteQueue(models.Model):
    experiment_id = models.IntegerField(db_index=True)
    pid = models.IntegerField(db_index=True, default=0)
    status = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

