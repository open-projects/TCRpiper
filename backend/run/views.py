from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def run(request, run_id):
    print(run_id)
    template = loader.get_template('run.html')
    return HttpResponse(template.render())