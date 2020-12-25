from django.urls import path, include
from django.contrib import admin

from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('', include("accounts.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls'))
]

