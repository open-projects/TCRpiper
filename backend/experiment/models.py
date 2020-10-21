'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models

from sample.models import Sample


EXPERIMENT_STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))
WORKFLOW_TYPE = (('GenerateFASTQ', 'Generate FASTQ'), ('other', 'Other'))
APPLICATION_TYPE = (('FASTQ Only', 'FASTQ Only'), ('other', 'Other'))
ASSAY_TYPE = (('TruSeq HT', 'TruSeq HT'), ('other', 'Other'))
CHEMISTRY = (('Amplicon', 'Amplicon'), ('other', 'Other'))
REVCOMPL = (('0', 'No'), ('1', 'Yes'))
DEFAULT_READS = 166
FILE_VERSION = 4


class Experiment(models.Model):
    status = models.CharField(max_length=200, choices=EXPERIMENT_STATUS, default='open')
    # [Header]
    iem_file_version = models.CharField(max_length=200, default=FILE_VERSION)
    name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    workflow = models.CharField(max_length=200, choices=WORKFLOW_TYPE, default='GenerateFASTQ')
    application = models.CharField(max_length=200, choices=APPLICATION_TYPE, default='FASTQ Only')
    assay = models.CharField(max_length=200, choices=ASSAY_TYPE, default='TruSeq HT')
    chemistry = models.CharField(max_length=200, choices=CHEMISTRY, default='Amplicon')
    description = models.TextField(default='')
    # [Reads]
    reads_1 = models.IntegerField(default=0)
    reads_2 = models.IntegerField(default=0)
    # [Settings]
    rev_compl = models.IntegerField(choices=REVCOMPL, default=0)
    # adapter = models.CharField(max_length=200, default='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
    # adapter_read2 = models.CharField(max_length=200, default='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT')

    def num_of_samples(self):
        sample_list = Sample.objects.filter(experiment_id=self.id)
        return len(sample_list)

    def is_pared(self):
        if self.reads_1 and self.reads_2:
            return True
        return False

