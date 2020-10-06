from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Stock


def index(request):
    #  data request
    run_list = Stock.objects.order_by('id').reverse()
    context = {
        'run_list': run_list,
        'num_of_runs': len(run_list),
    }
    return render(request, 'stock.html', context)

