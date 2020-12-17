'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.conf import settings


PYTHON_PATH = '/usr/bin/python3'

PIPER_PATH = '/home/user/PycharmProjects/TCRpiper/'
PIPER_NAME = 'tcrpiper.py'
MAX_MEMORY = '20G'
OUT_DIRNAME = 'output'
LOG_FILE = 'pipeline.log'

PIPER = ''.join((PYTHON_PATH, ' ', PIPER_PATH, PIPER_NAME))

