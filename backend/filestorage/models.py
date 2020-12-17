'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
from django.db import models


def path2dir(instance, filename):
    # a file will be uploaded to MEDIA_ROOT/experiment_<id>/<filename>
    return 'experiment_{}/{}'.format(instance.experiment_id, filename)


class File(models.Model):
    experiment_id = models.IntegerField(db_index=True, default=0)
    file = models.FileField(upload_to=path2dir)
    date = models.DateTimeField(auto_now_add=True)

