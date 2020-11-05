from __future__ import unicode_literals

from django.db import models


class File(models.Model):
    experiment_id = models.IntegerField(default=0)
    file = models.FileField(upload_to='sequences/')
    date = models.DateTimeField(auto_now_add=True)
