"""
TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
"""
from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('index.urls')),
    path(r'primers/', include('primers.urls')),
    path(r'project/', include('project.urls')),
    path(r'run/', include('run.urls')),
    #re_path(r'^$', include('tcrpiper.urls')),
]

