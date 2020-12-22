'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.conf import settings


EXPERIMENT_STATUS = (('open', 'Open'), ('closed', 'Closed'), ('archived', 'Archived'))
RESULT_STATUS = (('incomplete', 'Incomplete'), ('ongoing', 'Ongoing'), ('ready', 'Ready'))
WORKFLOW_TYPE = (('GenerateFASTQ', 'Generate FASTQ'), ('other', 'Other'))
APPLICATION_TYPE = (('FASTQ Only', 'FASTQ Only'), ('other', 'Other'))
ASSAY_TYPE = (('TruSeq HT', 'TruSeq HT'), ('other', 'Other'))
CHEMISTRY = (('Amplicon', 'Amplicon'), ('other', 'Other'))
REVCOMPL = (('0', 'No'), ('1', 'Yes'))
DEFAULT_READS = 166
FILE_VERSION = 4