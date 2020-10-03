from django.urls import path

from . import views

app_name = 'primers'
urlpatterns = [
    path('', views.index, name='primers'),
]
