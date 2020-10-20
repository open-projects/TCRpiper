'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse

from .models import Experiment, APPLICATION_TYPE, WORKFLOW_TYPE, ASSAY_TYPE, CHEMISTRY, REVCOMPL, DEFAULT_READS, FILE_VERSION
from sample.models import Sample


def stock(request):
    experiment_list = Experiment.objects.order_by('id').reverse()
    context = {
        'experiment_list': experiment_list,
        'num_of_experiments': len(experiment_list),
    }

    return render(request, 'experiment_stock.html', context)


def set(request, experiment_id=0):
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            raise Http404("Experiment does not exist")

        experiment.status = request.POST['experiment_status']
        experiment.iem_file_version = request.POST['iem_file_version']
        experiment.name = str(request.POST['experiment_name'])
        experiment.workflow = request.POST['workflow']
        experiment.application = request.POST['application']
        experiment.assay = request.POST['assay']
        experiment.chemistry = request.POST['chemistry']
        experiment.description = request.POST['description']
        experiment.reads_1 = int(request.POST['reads_1'])
        experiment.reads_2 = int(request.POST['reads_2']) if request.POST['reads_2'] else 0
        experiment.rev_compl = request.POST['rev_compl']

        experiment.save()

    else:
        try:
            experiment = Experiment(status=request.POST['experiment_status'],
                                    iem_file_version=request.POST['iem_file_version'],
                                    name=request.POST['experiment_name'],
                                    workflow=request.POST['workflow'],
                                    application=request.POST['application'],
                                    assay=request.POST['assay'],
                                    chemistry=request.POST['chemistry'],
                                    description=request.POST['description'],
                                    reads_1=request.POST['reads_1'],
                                    reads_2=request.POST['reads_2'] if request.POST['reads_2'] else 0,
                                    rev_compl=request.POST['rev_compl'],
                                   )
            experiment.save()
        except Exception:
            raise Http404("Bad request for New Experiment")

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))


def get(request, experiment_id=0):
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            raise Http404("Experiment does not exist")

        sample_list = Sample.objects.filter(experiment_id=experiment.id)
        context = {
            'experiment_id': experiment.id,
            'experiment_status': experiment.status,
            'iem_file_version': experiment.iem_file_version,
            'experiment_name': experiment.name,
            'description': experiment.description,

            'workflow': experiment.workflow,
            'application': experiment.application,
            'assay': experiment.assay,
            'chemistry': experiment.chemistry,
            'rev_compl': str(experiment.rev_compl),  # str() is important !!!

            'workflow_list': WORKFLOW_TYPE,
            'application_list': APPLICATION_TYPE,
            'assay_list': ASSAY_TYPE,
            'chemistry_list': CHEMISTRY,
            'rev_compl_list': REVCOMPL,
            'reads_1': experiment.reads_1,
            'reads_2': experiment.reads_2,
            'sample_list': sample_list,
            'num_of_samples': len(sample_list)
        }
    else:
        context = {
            'experiment_id': 0,
            'experiment_status': 'open',
            'iem_file_version': FILE_VERSION,
            'experiment_name': '',
            'description': '',

            'workflow': None,
            'application': None,
            'assay': None,
            'chemistry': None,
            'rev_compl': None,

            'workflow_list': WORKFLOW_TYPE,
            'application_list': APPLICATION_TYPE,
            'assay_list': ASSAY_TYPE,
            'chemistry_list': CHEMISTRY,
            'rev_compl_list': REVCOMPL,
            'reads_1': DEFAULT_READS,
            'reads_2': DEFAULT_READS,
            'sample_list': list(),
            'num_of_samples': 0
        }
    return render(request, 'experiment.html', context)


def delete(request, experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Exception:
        raise Http404("Experiment does not exist")

    for sample in Sample.objects.filter(experiment_id=experiment_id):
        sample.delete()

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

