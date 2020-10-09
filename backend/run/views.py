from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse

from .models import Run
from project.models import Project


def stock(request):
    run_list = Run.objects.order_by('id').reverse()
    context = {
        'run_list': run_list,
        'num_of_runs': len(run_list),
    }

    return render(request, 'run_stock.html', context)


def new(request):
    try:
        run_name = request.POST['run_name']
    except Exception:
        raise Http404("No run name")
    run = Run(name=run_name)
    run.save()

    return HttpResponseRedirect(reverse('run:run_stock'))


def get(request, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Exception:
        raise Http404("Run does not exist")

    project_list = Project.objects.filter(run_id=run.id)
    context = {
        'run_id': run_id,
        'run_status': run.status,
        'project_list': project_list,
        'num_of_projects': len(project_list)
    }

    return render(request, 'run.html', context)


def delete(request, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Exception:
        raise Http404("Run does not exist")

    for project in Project.objects.filter(run_id=run_id):
        project.delete()

    run.delete()

    return HttpResponseRedirect(reverse('run:run_stock'))


def archive(request, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Exception:
        raise Http404("Run does not exist")
    run.status = 'archived'
    run.save()

    return HttpResponseRedirect(reverse('run:run_stock'))


def submit(request, run_id):
    try:
        run = Run.objects.get(id=run_id)
    except Exception:
        raise Http404("Run does not exist")
    run.status = 'closed'
    run.save()

    return HttpResponseRedirect(reverse('run:run_stock'))

