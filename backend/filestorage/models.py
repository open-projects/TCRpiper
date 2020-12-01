from __future__ import unicode_literals

from django.db import models


def path2dir(instance, filename):
    # file will be uploaded to MEDIA_ROOT/experiment_<id>/<filename>
    return 'experiment_{0}/{1}'.format(instance.experiment_id, filename)


class File(models.Model):
    experiment_id = models.IntegerField(default=0)
    file = models.FileField(upload_to=path2dir)
    date = models.DateTimeField(auto_now_add=True)
