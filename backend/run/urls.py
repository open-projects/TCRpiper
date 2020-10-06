from django.urls import path

from . import views

app_name = 'run'
urlpatterns = [
    path('', views.stock, name='run_stock'),
    path('new/', views.new, name='run_new'),
    path('get/<int:run_id>/', views.get, name='run_get'),
]
