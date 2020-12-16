'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

import re
from django.db import models
from pipeline import settings as pipelne_settings
from configurator.models import makeSampleinfo
from filestorage.models import File


class Executer:
    def __init__(self, parameters={}):
        self._piper = pipelne_settings.PIPER
        self._parameters = parameters


    def run(self, experiment):
        file_item = File.objects.filter(experiment_id=experiment.id).first()
        if '-i' not in self._parameters:
            self._parameters['-i'] = re.sub(r'/[^/]*$', '/', file_item.file.path)
        if '-o' not in self._parameters:
            self._parameters['-o'] = self._parameters['-i'] + pipelne_settings.OUT_DIRNAME
        if '-l' not in self._parameters:
            self._parameters['-l'] = '/'.join((self._parameters['-o'], pipelne_settings.LOG_FILE))
        if '-m' not in self._parameters:
            self._parameters['-m'] = pipelne_settings.MAX_MEMORY


        sampleInfo = makeSampleinfo(experiment)




        prm = ' '.join('{} {}'.format(key, value) for key, value in self._parameters.items())
        cmd = ' '.join((self._piper, prm))
        return cmd
