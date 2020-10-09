'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models


class Smart(models.Model):
    number = models.IntegerField(unique=True)
    seq = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)
    comment = models.TextField(blank=True)


class Index(models.Model):
    number = models.IntegerField(unique=True)
    seq = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200, blank=True)
    date = models.DateField(blank=True)
    comment = models.TextField(blank=True)

