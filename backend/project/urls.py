from django.urls import path

from . import views

urlpatterns = [
    path('get/<int:project_id>/', views.get, name='project_get'),
    path('set/<int:project_id>/', views.set, name='project_set'),
    path('del/<int:project_id>/', views.delete, name='project_del'),
]
