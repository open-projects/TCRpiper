from django.urls import path

from . import views

app_name = 'run'
urlpatterns = [
    path('get/<int:run_id>/', views.run, name='run_get'),
]
