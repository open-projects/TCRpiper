'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

import re
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
        raise Http404("Sample does not exist")
    sample.delete()

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))


def get(request, experiment_id, sample_id=0):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    alfa_index_list = Index.objects.filter(type='alfa').order_by('id')
    beta_index_list = Index.objects.filter(type='beta').order_by('id')
    smart_list = Smart.objects.order_by('id')
    context = {  # for project creation
        'experiment_id': experiment.id,
        'sample_id': 0,
        'alfa_subsample_ident': 'alfa',
        'beta_subsample_ident': 'beta',
        'alfa_index_list': alfa_index_list,
        'beta_index_list': beta_index_list,
        'smart_list': smart_list,
    }

    used_barcodes = IdContainer()
    for sample in Sample.objects.filter(experiment_id=experiment_id):
        if sample.id == sample_id:
            context = {  # for project modification
                'experiment_id': sample.experiment_id,
                'sample_id': sample.id,
                'sample_project': sample.project,
                'sample_ident': sample.ident,
                'sample_name': sample.name,
                'sample_plate': sample.plate,
                'sample_well': sample.well,
                'cell_number': sample.cell_number,
                'read_number': sample.read_number,
                'smart_name':  sample.smart_name,
                'alfa_subsample_ident': sample.alfa_subsample_ident,
                'alfa_index_name': sample.alfa_index_name,
                'beta_subsample_ident': sample.beta_subsample_ident,
                'beta_index_name': sample.beta_index_name,
                'comments': sample.comments,
                'alfa_index_list': alfa_index_list,
                'beta_index_list': beta_index_list,
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
            raise Http404("Sample does not exist")

        try:
            sample.experiment_id = experiment.id
            sample.project = re.sub(r'[ _]+', '_', request.POST['sample_project'])
            sample.ident = re.sub(r'[ _]+', '_', request.POST['sample_ident'])
            sample.name = request.POST['sample_name']
            sample.plate = request.POST['sample_plate']
            sample.well = request.POST['sample_well']
            sample.cell_number = request.POST['cell_number']
            sample.read_number = request.POST['read_number']
            sample.smart_name = request.POST['smart_name']
            sample.alfa_subsample_ident = request.POST['alfa_subsample_ident']
            sample.alfa_index_name = request.POST['alfa_index_name']
            sample.beta_subsample_ident = request.POST['beta_subsample_ident']
            sample.beta_index_name = request.POST['beta_index_name']
            sample.comments = request.POST['comments']
            sample.save()
        except Exception as e:
            raise Http404("Bad request for Sample")

    else:
        #  project creation
        try:
            sample = Sample(experiment_id=experiment.id,
                              project=re.sub(r'[ _]+', '_', request.POST['sample_project']),
                              ident=re.sub(r'[ _]+', '_', request.POST['sample_ident']),
                              name=request.POST['sample_name'],
                              plate=request.POST['sample_plate'],
                              well=request.POST['sample_well'],
                              cell_number=request.POST['cell_number'] if request.POST['cell_number'] else 0,
                              read_number=request.POST['read_number'] if request.POST['read_number'] else 0,
                              smart_name=request.POST['smart_name'],
                              alfa_subsample_ident=request.POST['alfa_subsample_ident'],
                              alfa_index_name=request.POST['alfa_index_name'],
                              beta_subsample_ident=request.POST['beta_subsample_ident'],
                              beta_index_name=request.POST['beta_index_name'],
                              comments='comments'
                             )
            sample.save()
        except Exception:
            raise Http404("Bad request for New Sample")

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))


def save(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))

