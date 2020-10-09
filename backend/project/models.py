'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models


class Project(models.Model):
    run_id = models.IntegerField()
    name = models.CharField(max_length=200)
    sample_id = models.IntegerField()
    sample_number = models.IntegerField(default=0)  # reserved
    sample_name = models.CharField(max_length=200)
    cell_number = models.IntegerField(default=0)
    read_number = models.IntegerField(default=0)
    smart_id = models.IntegerField()
    alfa_subsample_id = models.IntegerField()
    alfa_subsample_name = models.CharField(max_length=200, default='')  # reserved
    alfa_index_id = models.IntegerField()
    alfa_index_number = models.IntegerField(default=0)  # reserved
    beta_subsample_id = models.IntegerField()
    beta_subsample_name = models.CharField(max_length=200, default='')  # reserved
    beta_index_id = models.IntegerField()
    beta_index_number = models.IntegerField(default=0)  # reserved
    comments = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    owner = models.CharField(max_length=200, default='Unknown')


class UsedBarcode:
    def __init__(self, project):
        self.project_id = project.id
        self.owner = project.owner
        self.smart_id = project.smart_id
        self.alfa_index_id = project.alfa_index_id
        self.beta_index_id = project.beta_index_id


class IdContainer:
    def __init__(self):
        self.barcodes = list()
        self.smarts = set()
        self.indexes = set()

    def append(self, barcode):
        self.barcodes.append(barcode)
        self.smarts.add(barcode.smart_id)
        self.indexes.add(barcode.alfa_index_id)
        self.indexes.add(barcode.beta_index_id)

