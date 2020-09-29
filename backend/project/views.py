from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from primers.models import Smart, Index


def project(request):
    template = loader.get_template('project.html')
    return HttpResponse(template.render())


def index(request):
    index_list = Index.objects.order_by('id')
    smart_list = Smart.objects.order_by('id')

    if request.POST:
        1

    else:
        # delete data from models
        1
    context = {
        'index_list': index_list,
        'smart_list': smart_list,
    }

    return render(request, 'project.html', context)

