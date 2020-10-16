'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models

from project.models import Project


EXPERIMENT_STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))
WORKFLOW_TYPE = (('GenerateFASTQ', 'GenerateFASTQ'), ('other', 'Other'))
APPLICATION_TYPE = (('FASTQ Only', 'FASTQ Only'), ('other', 'Other'))
ASSAY_TYPE = (('TruSeq HT', 'TruSeq HT'), ('other', 'Other'))


class Experiment(models.Model):
    status = models.CharField(max_length=200, choices=EXPERIMENT_STATUS, default='open')
    # [Header]
    iem_file_version = models.CharField(max_length=200, default='4')
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    workflow = models.CharField(max_length=200, choices=WORKFLOW_TYPE, default='GenerateFASTQ')
    application = models.CharField(max_length=200, choices=APPLICATION_TYPE, default='FASTQ Only')
    assay = models.CharField(max_length=200, choices=ASSAY_TYPE, default='TruSeq HT')
    description = models.TextField(default='')
    # [Reads]
    reads_1 = models.IntegerField(default=166)
    reads_2 = models.IntegerField(default=166)
    # [Settings]
    rev_compl = models.IntegerField(default=0)
    # adapter = models.CharField(max_length=200, default='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
    # adapter_read2 = models.CharField(max_length=200, default='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT')

    def num_of_projects(self):
        project_list = Project.objects.filter(run_id=self.id)
        return len(project_list)

