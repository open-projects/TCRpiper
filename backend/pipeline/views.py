'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
import subprocess

from django.core.files.base import ContentFile
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404

from experiment.models import Experiment
from pipeline import settings as pipelne_settings
from configurator.models import makeSampleinfo
from configurator.settings import SAMPLE_INFO_FILENAME, SAMPLE_INFO_PATTERN
from filestorage.models import File
from . models import TaskQueue, taskRemover

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
    log_file = output_path + '/' + pipelne_settings.LOG_FILE
    compressed_file = input_path + '/' + pipelne_settings.OUT_FILE
    cmd_array = [pipelne_settings.PYTHON_PATH,
                 pipelne_settings.PIPER_PATH,
                 '-m', pipelne_settings.MAX_MEMORY,
                 '-i', input_path,
                 '-o', output_path,
                 '-l', log_file,
                 '-z', compressed_file,
                 '-p', str(pipelne_settings.PORT),
                 '-r',
                 ]
    cmd_string = ' '.join(cmd_array)

    taskRemover()  # remove completed tasks
    new_task = None
    for k in range(pipelne_settings.THREADS):  # find an empty slot for the new task
        task_in_process = TaskQueue.objects.filter(thread=k).first()
        if not task_in_process:
            try:
                new_task = TaskQueue(experiment_id=experiment.id,
                                     thread=k,
                                     cmd=cmd_string,
                                     output_file=compressed_file
                                     )
                new_task.save()
            except Exception:
                continue
            else:
                break
    if new_task:
        try:
            process = subprocess.Popen(cmd_array, stdin=None, stdout=None, stderr=None, shell=False, close_fds=True)
        except Exception:
            raise Http404("Can't run a new process!")
        else:
            try:
                new_task.pid = process.pid
                new_task.save()
            except Exception:
                raise Http404("Can't update the process status!")
            else:
                try:
                    experiment.output_file = compressed_file
                    experiment.output_dir = output_path
                    experiment.output_status = 'ongoing'
                    experiment.save()
                except Exception:
                    return HttpResponseRedirect(reverse('experiment:experiment_stock'))
    else:
        context = {
            'cmd': "All server slots are taken! Try later...",
        }

    return HttpResponseRedirect(reverse('experiment:experiment_stock'))

