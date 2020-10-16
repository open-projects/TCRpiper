'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse

from .models import Experiment
from project.models import Project


def stock(request):
    experiment_list = Experiment.objects.order_by('id').reverse()
    context = {
        'experiment_list': experiment_list,
        'num_of_experiments': len(experiment_list),
    }

    return render(request, 'experiment_stock.html', context)


def new(request):
    try:
        experiment_name = request.POST['experiment_name']
    except Exception:
        raise Http404("No experiment name")
    experiment = Experiment(name=experiment_name)
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def get(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    project_list = Project.objects.filter(run_id=experiment.id)
    context = {
        'experiment_id': experiment_id,
        'experiment_status': experiment.status,
        'project_list': project_list,
        'num_of_projects': len(project_list)
    }

    return render(request, 'experiment.html', context)


def delete(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    for project in Project.objects.filter(run_id=experiment_id):
        project.delete()

    experiment.delete()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def archive(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")
    experiment.status = 'archived'
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def submit(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")
    experiment.status = 'closed'
    experiment.save()

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))

