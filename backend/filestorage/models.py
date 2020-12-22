'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
import os
from django.db import models
from django.conf import settings


def path2dir(instance, filename):
    # a file will be uploaded to MEDIA_ROOT/experiment_<id>/<filename>
    return 'experiment_{}/{}'.format(instance.experiment_id, filename)


class File(models.Model):
    experiment_id = models.IntegerField(db_index=True, default=0)
    file = models.FileField(upload_to=path2dir)
    date = models.DateTimeField(auto_now_add=True)


def cleanup(experiment_id):
    files = list()
    for item in File.objects.filter(experiment_id=experiment_id):
        files.append(item.file.url)
        item.file.delete()
        item.delete()

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):  # cleanup empty dirs
        for d in dirs:
            dir = os.path.join(root, d)
            if not os.listdir(dir):  # check if dir is empty
                os.rmdir(dir)

    return files

