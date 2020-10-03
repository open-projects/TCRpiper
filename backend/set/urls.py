from django.urls import path

from . import views

app_name = 'set'
urlpatterns = [
    path('', views.set, name='set'),
]
