from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django import forms

from .models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )


class FileUploadView(View):
    def get(self, request):
        file_list = File.objects.all()
        context = {'file_list': file_list}
        return render(self.request, 'filestorage.html', context)

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
    for item in File.objects.all():
        item.file.delete()
        item.delete()
    return redirect(request.POST.get('next'))
