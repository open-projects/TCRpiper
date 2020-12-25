from django.urls import path
from django.contrib import admin

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name="home"),
    path('accounts/sign_up/', views.sign_up, name="sign-up"),

    path(r'new/', views.new, name='accounts_new'),
    path(r'get/', views.get, name='accounts_get'),
]

