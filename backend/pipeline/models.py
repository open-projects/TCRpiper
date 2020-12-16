'''
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
'''

from django.db import models
from pipeline import settings as pipelne_settings
from configurator.models import makeSampleinfo
from filestorage.models import File


class Executer:
    def __init__(self, parameters={}):
        self._piper = pipelne_settings.PIPER
        self._parameters = parameters


    def run(self, experiment):
        sampleInfo = makeSampleinfo(experiment)
        for item in File.objects.filter(experiment_id=experiment.id):
            item

        prm = ' '.join('{} {}'.format(key, value) for key, value in self._parameters.items())
        cmd = ' '.join((self._piper, prm))
        return cmd
