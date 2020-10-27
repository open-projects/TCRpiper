'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from experiment.models import Experiment
from sample.models import Sample


def samplesheet(request, experiment_id=0):
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    sample_list = Sample.objects.filter(experiment_id=experiment_id).order_by('id')  # ordering is important !
    context = {
        'experiment': experiment,
        'sample_list': sample_list,
    }
    message = render_to_string('SampleSheet.csv', context)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="SampleSheet.csv"'
    response.write(message)

    return response

def sampleinfo(request, experiment_id=0):
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    paired = experiment.is_pared()

    n = 1
    sample_stings = list()
    for sample in  Sample.objects.filter(experiment_id=experiment_id).order_by('id'):  # ordering is important !
        if sample.alfa_index_name:
            alfa_name = sample.get_alfa_name()
            chain = 'TRA'
            barcodes = sample.get_smart_seqcore()
            r1 = '_'.join((sample.get_alfa_name(), 'S' + str(n), 'L001', 'R1', '001.fastq.gz '))
            r2 = ''
            if paired:
                r2 = '_'.join((sample.get_alfa_name(), 'S' + str(n), 'L001', 'R2', '001.fastq.gz '))
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_stings.append('\t'.join((alfa_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

        if sample.beta_index_name:
            beta_name = sample.get_beta_name()
            chain = 'TRB'
            barcodes = sample.get_smart_seqcore()
            r1 = '_'.join((sample.get_beta_name(), 'S' + str(n), 'L001', 'R1', '001.fastq.gz'))
            r2 = ''
            if paired:
                r2 = '_'.join((sample.get_beta_name(), 'S' + str(n), 'L001', 'R2', '001.fastq.gz'))
            baseline = ''
            subject_id = ''
            antigen = ''
            reads_exp = sample.read_number

            sample_stings.append('\t'.join((beta_name, chain, barcodes, r1, r2, baseline, subject_id, antigen, str(reads_exp))))
            n += 1

    context = {
        'sample_stings': sample_stings,
    }

    message = render_to_string('SampleInfo.csv', context)

    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment; filename="Sample_Info.txt"'
    response.write(message)

    return response

