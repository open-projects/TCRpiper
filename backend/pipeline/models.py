'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
import subprocess
from django.db import models
from django.core.files.base import ContentFile
from pipeline import settings as pipelne_settings
from configurator.models import makeSampleinfo
from configurator.settings import SAMPLE_INFO_FILENAME, SAMPLE_INFO_PATTERN
from filestorage.models import File


class Executer:
    def __init__(self, parameters={}):
        self._piper = pipelne_settings.PIPER
        self._parameters = parameters

    def run(self, experiment):
        file_item = File.objects.filter(experiment_id=experiment.id, file__regex=SAMPLE_INFO_PATTERN)
        if not file_item:
            sample_info = ContentFile(makeSampleinfo(experiment))
            sample_info.name = SAMPLE_INFO_FILENAME
            sample_info_file = File(experiment_id=experiment.id, file=sample_info)
            sample_info_file.save()

        file_item = File.objects.filter(experiment_id=experiment.id).first()
        if '-i' not in self._parameters:
            self._parameters['-i'] = re.sub(r'/[^/]*$', '/', file_item.file.path)
        if '-o' not in self._parameters:
            self._parameters['-o'] = self._parameters['-i'] + pipelne_settings.OUT_DIRNAME
        if '-l' not in self._parameters:
            self._parameters['-l'] = '/'.join((self._parameters['-o'], pipelne_settings.LOG_FILE))
        if '-m' not in self._parameters:
            self._parameters['-m'] = pipelne_settings.MAX_MEMORY



        #useless_cat_call = subprocess.run(["pwd"], stdout=subprocess.PIPE)
        #print(useless_cat_call.stdout)

        #prm = ' '.join('{} {}'.format(key, value) for key, value in self._parameters.items())
        cmd = pipelne_settings.PIPER_PATH + pipelne_settings.PIPER_NAME + ' ' + ' '.join('{} {}'.format(key, value) for key, value in self._parameters.items())
        cmd_array = [pipelne_settings.PYTHON_PATH,
                    pipelne_settings.PIPER_PATH + pipelne_settings.PIPER_NAME,
                    '-i', re.sub(r'/[^/]*$', '/', file_item.file.path),
                    '-o', re.sub(r'/[^/]*$', '/', file_item.file.path) + pipelne_settings.OUT_DIRNAME
                    ]
        #useless_cat_call = subprocess.run(cmd_array)
        #print(useless_cat_call.stdout)

        #print("!!!!!!!!!!!!RUN")

        return ' '.join(cmd_array)

