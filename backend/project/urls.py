'''
TCRpiper - a pipeline for TCR sequence treatment. Copyright (C) 2020  D. Malko
'''

from django.urls import path

from . import views


app_name = 'project'
urlpatterns = [
    path('get/<int:run_id>/', views.get, name='project_new'),
    path('get/<int:run_id>/<int:project_id>/', views.get, name='project_get'),
    path('set/<int:run_id>/<int:project_id>/', views.set, name='project_set'),
    path('del/<int:run_id>/<int:project_id>/', views.delete, name='project_del'),
]
