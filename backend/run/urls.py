from django.urls import path

from . import views

app_name = 'run'
urlpatterns = [
    path('', views.stock, name='run_stock'),
    path('new/', views.new, name='run_new'),
    path('get/<int:run_id>/', views.get, name='run_get'),
    path('del/<int:run_id>/', views.delete, name='run_del'),
    path('arch/<int:run_id>/', views.archive, name='run_arch'),
    path('sub/<int:run_id>/', views.submit, name='run_sub'),
]
