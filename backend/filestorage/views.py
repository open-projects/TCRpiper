import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django import forms
from django.conf import settings

from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('experiment_id', 'file', )


class FileUploadView(View):
    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            data = form.save()
            context = {
                'is_valid': True,
                'name': data.file.name,
                'url': data.file.url
            }
        else:
            context = {'is_valid': False}
        return JsonResponse(context)


def data_cleanup(request):
    for item in File.objects.filter(experiment_id=request.POST.get('experiment_id')):
        item.file.delete()
        item.delete()

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):  # cleanup empty dirs
        for d in dirs:
            dir = os.path.join(root, d)
            if not os.listdir(dir):  # check if dir is empty
                os.rmdir(dir)
    return redirect(request.POST.get('next'))

