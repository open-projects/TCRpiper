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
            raise Http404("Experiment does not exist")

    sample_list = Sample.objects.filter(experiment_id=experiment_id)
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

    return 1



