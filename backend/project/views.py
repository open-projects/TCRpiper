from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import Http404
from django.template import loader

from .models import Project
from primers.models import Smart, Index


def delete(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    run_id = project.run_id  # save to redirect to Run page
    project.delete()

    return HttpResponseRedirect('/run/get/1/')


def get(request, project_id):
    if project_id:  # project modification
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        context = {
            'run_id': project.run_id,
            'project_id': project_id,
            'project_name': project.project_name,
            'sample_id': project.sample_id,
            'sample_name': project.sample_name,
            'cell_number': project.cell_number,
            'read_number': project.read_number,
            'smart_id':  project.smart_id,
            'alfa_subsample_id': project.alfa_subsample_id,
            'alfa_index_id': project.alfa_index_id,
            'beta_subsample_id': project.beta_subsample_id,
            'beta_index_id': project.beta_index_id,
            'comments': project.comments,
            'index_list': Index.objects.order_by('id'),
            'smart_list': Smart.objects.order_by('id'),
        }

    else:  # project creation
        run_id = 1
#        try:
#            run_id = request.POST['run_id']
#        except Exception:
#            raise Http404("Run is not determined")

        context = {
            'run_id': run_id,
            'project_id': 0,
            'index_list': Index.objects.order_by('id'),
            'smart_list': Smart.objects.order_by('id'),
        }

    return render(request, 'project.html', context)


def set(request, project_id):
    try:
        run_id = request.POST['run_id']
    except Exception:
        raise Http404("Run is not determined")

    if project_id:  # project modification
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise Http404("Project does not exist")
        try:
            project.run_id = run_id
            project.project_name = request.POST['project_name']
            project.sample_id = request.POST['sample_id']
            project.sample_name = request.POST['sample_name']
            project.cell_number = request.POST['cell_number']
            project.read_number = request.POST['read_number']
            project.smart_id = request.POST['smart_id']
            project.alfa_subsample_id = request.POST['alfa_subsample_id']
            project.alfa_index_id = request.POST['alfa_subsample_id']
            project.beta_subsample_id = request.POST['beta_subsample_id']
            project.beta_index_id = request.POST['beta_index_id']
            project.comments = request.POST['comments']
            project.save()
        except Exception as e:
            raise Http404("Bad request for Project")

    else:  # project creation
        try:
            project = Project(run_id=run_id,
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
            project.save()
        except Exception:
            raise Http404("Bad request for New Project")

    return HttpResponseRedirect('/run/get/1/')

