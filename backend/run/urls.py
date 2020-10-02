from django.urls import path

from . import views

urlpatterns = [
    path('get/<int:run_id>/', views.run, name='run_get'),
]
