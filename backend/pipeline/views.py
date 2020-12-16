'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.shortcuts import render
from . models import Executer
from filestorage.models import path2dir

def get(request):
    path2dir()
    exe = Executer(parameters={'-i': 'input', '-o': 'ouput', '-m': '20G', '-l': 'log.log'})
    context = {
        'cmd': exe.run(),
    }

    return render(request, 'pipeline.html', context)

