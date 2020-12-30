'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

import re
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404

from .models import Sample, UsedBarcode, IdContainer
from experiment.models import Experiment
from primers.models import Smart, Index


def delete(request, experiment_id, sample_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    try:
        sample = Sample.objects.get(id=sample_id)
    except Sample.DoesNotExist:
        raise Http404("Sample does not exist")

    sample.delete()

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))


def get(request, experiment_id, sample_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    alfa_index_list = Index.objects.filter(type='alfa').order_by('name')
    beta_index_list = Index.objects.filter(type='beta').order_by('name')
    smart_list = Smart.objects.order_by('name')
    context = {  # for project creation
        'experiment_id': experiment.id,
        'sample_id': 0,
        'alfa_subsample_ident': 'alfa',
        'beta_subsample_ident': 'beta',
        'alfa_index_list': alfa_index_list,
        'beta_index_list': beta_index_list,
        'smart_list': smart_list,
        'experiment_status': experiment.status,
    }

    used_barcodes = IdContainer()
    for sample in Sample.objects.filter(experiment_id=experiment_id).order_by('id'):
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
                'smart_benchling': sample.smart_benchling,
                'alfa_subsample_ident': sample.alfa_subsample_ident,
                'alfa_index_name': sample.alfa_index_name,
                'alfa_index_benchling': sample.alfa_index_benchling,
                'beta_subsample_ident': sample.beta_subsample_ident,
                'beta_index_name': sample.beta_index_name,
                'beta_index_benchling': sample.beta_index_benchling,
                'comments': sample.comments,
                'alfa_index_list': alfa_index_list,
                'beta_index_list': beta_index_list,
                'smart_list': smart_list,
                'experiment_status': experiment.status,
            }
        barcode = UsedBarcode(sample)
        used_barcodes.append(barcode)

    context['used_barcodes'] = used_barcodes
    return render(request, 'sample.html', context)


def set(request, experiment_id, sample_id=0):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    user = request.user

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    if sample_id:
        #  sample modification
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
            sample.smart_benchling = request.POST['smart_benchling']
            sample.alfa_subsample_ident = request.POST['alfa_subsample_ident']
            sample.alfa_index_name = request.POST['alfa_index_name']
            sample.alfa_index_benchling = request.POST['alfa_index_benchling']
            sample.beta_subsample_ident = request.POST['beta_subsample_ident']
            sample.beta_index_name = request.POST['beta_index_name']
            sample.beta_index_benchling = request.POST['beta_index_benchling']
            sample.comments = request.POST['comments']
            sample.owner = user
            sample.save()
        except Exception as e:
            raise Http404("Bad request for Sample")

    else:
        #  sample creation
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
                              smart_benchling = request.POST['smart_benchling'],
                              alfa_subsample_ident=request.POST['alfa_subsample_ident'],
                              alfa_index_name=request.POST['alfa_index_name'],
                              alfa_index_benchling=request.POST['alfa_index_benchling'],
                              beta_subsample_ident=request.POST['beta_subsample_ident'],
                              beta_index_name=request.POST['beta_index_name'],
                              beta_index_benchling=request.POST['beta_index_benchling'],
                              comments='comments',
                              owner=user
                             )
            sample.save()
        except Exception:
            raise Http404("Bad request for New Sample")

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))


def save(request, experiment_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index:index'))

    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        #raise Http404("Experiment does not exist")
        return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    return HttpResponseRedirect(reverse('experiment:experiment_get', args=(experiment.id,)))

