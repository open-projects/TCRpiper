'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
import subprocess

from django.core.files.base import ContentFile
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from experiment.models import Experiment
from pipeline import settings as pipelne_settings
from configurator.models import makeSampleinfo
from configurator.settings import SAMPLE_INFO_FILENAME, SAMPLE_INFO_PATTERN
from filestorage.models import File
from . models import ExecuteQueue

def get(request, experiment_id=0):
    if experiment_id:
        try:
            experiment = Experiment.objects.get(id=experiment_id)
        except Exception:
            #raise Http404("Experiment does not exist")
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))

    file_item = File.objects.filter(experiment_id=experiment.id, file__regex=SAMPLE_INFO_PATTERN)
    if not file_item:
        sample_info = ContentFile(makeSampleinfo(experiment))
        sample_info.name = SAMPLE_INFO_FILENAME
        sample_info_file = File(experiment_id=experiment.id, file=sample_info)
        sample_info_file.save()

    file_item = File.objects.filter(experiment_id=experiment.id).first()

    input_path = '.' + re.sub(r'/[^/]*$', '/', file_item.file.url)
    output_path = input_path + pipelne_settings.OUT_DIRNAME
    log_path = output_path + '/' + pipelne_settings.LOG_FILE
    cmd_array = [pipelne_settings.PYTHON_PATH,
                 pipelne_settings.PIPER_PATH,
                 '-i', input_path,
                 '-o', output_path,
                 '-l', log_path,
                 '-m', pipelne_settings.MAX_MEMORY,
                 '-z',
                 '-r',
                 ]
    process = subprocess.Popen(cmd_array)
    pid = process.pid

    context = {
        'cmd': 'cmd: ' + ' '.join(cmd_array) + '  pid: ' + str(pid),
    }

    return render(request, 'pipeline.html', context)

