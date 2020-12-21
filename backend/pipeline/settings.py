'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.conf import settings


PYTHON_PATH = 'python3'

PIPER_PATH = '../tcrpiper.py'
MAX_MEMORY = '6G'
OUT_DIRNAME = 'output'
OUT_FILE = 'output.tar.gz'
LOG_FILE = 'pipeline.log'
PORT = 10000
THREADS = 1  # 'MAX_MEMORY' X 'THREADS' < SYSTEM MEMORY !!!
