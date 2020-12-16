'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.conf import settings


PYTHON_PATH = 'python3'

PIPER_PATH = '../../'
PIPER_NAME = 'tcrpiper.py'
MAX_MEMORY = '20G'
LOG_FILE = 'output.log'

PIPER = ''.join((PYTHON_PATH, ' ', PIPER_PATH, PIPER_NAME))

