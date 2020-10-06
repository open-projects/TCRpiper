from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.template import loader

from .models import Run
from stock.models import Stock


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
    if run_id:
        print(run_id)

    else:  # create new run
        try:
            run_name = request.POST['run_name']
        except Exception:
            raise Http404("No run name")
        run = Run(name=run_name)
        run.save()
    return HttpResponseRedirect(reverse('run:run_stock'))
