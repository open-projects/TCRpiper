'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models
from primers.models import Smart, Index
import re


class Sample(models.Model):
    experiment_id = models.IntegerField()
    sample_project = models.CharField(max_length=200)
    sample_ident = models.CharField(max_length=200, unique=True)
    sample_name = models.CharField(max_length=200)
    sample_plate = models.CharField(max_length=200)
    sample_well = models.CharField(max_length=200)
    cell_number = models.IntegerField(default=0)
    read_number = models.IntegerField(default=0)
    smart_id = models.IntegerField(default=0)
    alfa_subsample_ident = models.CharField(max_length=200, default='')  # sample_ID = sample_ident + alfa_subsample_ident
    alfa_index_id = models.IntegerField(default=0)
    beta_subsample_ident = models.CharField(max_length=200, default='')  # sample_ID = sample_ident + beta_subsample_ident
    beta_index_id = models.IntegerField(default=0)
    comments = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    owner = models.CharField(max_length=200, default='Unknown')

    def type(self):
        if self.alfa_index_id == 0 and self.beta_index_id == 0:
            return 'ab'
        elif self.alfa_index_id == 0:
            return 'a'
        else:
            return 'b'

    def get_alfa_ident(self):
        ident = str(self.sample_ident) + '_' + str(self.alfa_subsample_ident)
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_beta_ident(self):
        ident = self.sample_ident + '_' + self.beta_subsample_ident
        ident = re.sub(r'[ _]+', '_', ident)
        return ident

    def get_smart(self):
        for smart in Smart.objects.filter(id=self.smart_id):
            return smart
        return None

    def get_smart_seqcore(self):
        for smart in Smart.objects.filter(id=self.smart_id):
            return smart.seqcore
        return ''

    def get_alfa_index(self):
        for index in Index.objects.filter(id=self.alfa_index_id):
            return index
        return None

    def get_alfa_index_seqcore(self):
        for index in Index.objects.filter(id=self.alfa_index_id):
            return index.seqcore
        return ''

    def get_beta_index(self):
        for index in Index.objects.filter(id=self.beta_index_id):
            return index
        return None

    def get_beta_index_seqcore(self):
        for index in Index.objects.filter(id=self.beta_index_id):
            return index.seqcore
        return ''


class UsedBarcode:
    def __init__(self, sample):
        self.sample_id = sample.id
        self.owner = sample.owner
        self.smart_id = sample.smart_id
        self.alfa_index_id = sample.alfa_index_id
        self.alfa_index_seqcore = sample.get_alfa_index_seqcore()
        self.beta_index_id = sample.beta_index_id
        self.beta_index_seqcore = sample.get_beta_index_seqcore()


class IdContainer:
    def __init__(self):
        self.barcodes = list()
        self.smarts = set()
        self.indexes = set()

    def append(self, barcode):
        self.barcodes.append(barcode)
        self.smarts.add(barcode.smart_id)
        self.seqcores.add(barcode.alfa_index_seqcore)
        self.seqcores.add(barcode.beta_index_seqcore)

