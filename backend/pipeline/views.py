'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from experiment.models import Experiment
from filestorage.models import path2dir
from . models import Executer

def get(request, experiment_id=0):
    #path2dir()
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    exe = Executer()
    context = {
        'cmd': exe.run(experiment),
    }

    return render(request, 'pipeline.html', context)

