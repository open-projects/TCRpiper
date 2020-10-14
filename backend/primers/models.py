'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models


INDEX_TYPE = (('alfa', 'Alfa'), ('beta', 'Beta'))


def norm_index_type(type):
    if len(type) > 0:
        type = type.lower()
        for itype in INDEX_TYPE:
            if type == itype[0]:
                return type
    return ''


class Smart(models.Model):
    name = models.CharField(max_length=200, unique=True)
    seq = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(default='')


class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=200, choices=INDEX_TYPE)
    seq = models.CharField(max_length=200, unique=True)
    source = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(default='')

