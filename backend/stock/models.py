from django.db import models


STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))
class Stock(models.Model):
    run_name = models.CharField(max_length=200)
    num_of_projects = models.IntegerField(blank=False)
    date = models.DateField(blank=False)
    status = models.CharField(max_length=200, choices=STATUS)

