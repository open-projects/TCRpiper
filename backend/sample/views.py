'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import Http404
from django.template import loader

from .models import Sample, UsedBarcode, IdContainer
from experiment.models import Experiment
from primers.models import Smart, Index


def delete(request, experiment_id, sample_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    try:
        sample = Sample.objects.get(id=sample_id)
    except Sample.DoesNotExist:
        raise Http404("Project does not exist")
    sample.delete()

    return HttpResponseRedirect(reverse(':experiment_get', args=(experiment.id,)))


def get(request, experiment_id, sample_id=0):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    index_list = Index.objects.order_by('id')
    smart_list = Smart.objects.order_by('id')
    context = {  # for project creation
        'experiment_id': experiment.id,
        'sample_id': 0,
        'index_list': index_list,
        'smart_list': smart_list,
    }

    used_barcodes = IdContainer()
    for sample in Sample.objects.filter(id=sample_id):
        if sample.id == sample_id:
            context = {  # for project modification
                'experiment_id': sample.experiment_id,
                'sample_project': sample.sample_project,
                'sample_ident': sample.sample_ident,
                'sample_name': sample.sample_name,
                'sample_palate': sample.sample_palate,
                'sample_well': sample.sample_well,
                'cell_number': sample.cell_number,
                'read_number': sample.read_number,
                'smart_id':  sample.smart_id,
                'alfa_subsample_id': sample.alfa_subsample_id,
                'alfa_index_id': sample.alfa_index_id,
                'beta_subsample_id': sample.beta_subsample_id,
                'beta_index_id': sample.beta_index_id,
                'comments': sample.comments,
                'index_list': index_list,
                'smart_list': smart_list,
            }
        barcode = UsedBarcode(sample)
        used_barcodes.append(barcode)

    context['used_barcodes'] = used_barcodes
    return render(request, 'sample.html', context)


def set(request, experiment_id, sample_id=0):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    if sample_id:
        #  project modification
        try:
            sample = Sample.objects.get(id=sample_id)
        except sample.DoesNotExist:
            raise Http404("Project does not exist")

        try:
            sample.experiment_id = experiment.id
            sample.project_name = request.POST['project_name']
            sample.sample_id = request.POST['sample_id']
            sample.sample_name = request.POST['sample_name']
            sample.cell_number = request.POST['cell_number']
            sample.read_number = request.POST['read_number']
            sample.smart_id = request.POST['smart_id']
            sample.alfa_subsample_id = request.POST['alfa_subsample_id']
            sample.alfa_index_id = request.POST['alfa_index_id']
            sample.beta_subsample_id = request.POST['beta_subsample_id']
            sample.beta_index_id = request.POST['beta_index_id']
            sample.comments = request.POST['comments']
            sample.save()
        except Exception as e:
            raise Http404("Bad request for Project")

    else:
        #  project creation
        try:
            sample = Sample(experiment_id=experiment.id,
                              project_name=request.POST['project_name'],
                              sample_id=request.POST['sample_id'],
                              sample_name=request.POST['sample_name'],
                              cell_number=request.POST['cell_number'],
                              read_number=request.POST['read_number'],
                              smart_id=request.POST['smart_id'],
                              alfa_subsample_id=request.POST['alfa_subsample_id'],
                              alfa_index_id=request.POST['alfa_subsample_id'],
                              beta_subsample_id=request.POST['beta_subsample_id'],
                              beta_index_id=request.POST['beta_index_id'],
                              comments=request.POST['comments']
                             )
            sample.save()
        except Exception:
            raise Http404("Bad request for New Project")

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))

