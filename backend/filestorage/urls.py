from django.conf.urls import url, include
from django.views.generic import TemplateView

from django.urls import path

from . import views

app_name = 'filestorage'
urlpatterns = [
    path(r'', TemplateView.as_view(template_name='home.html'), name='home'),
    path(r'clear/', views.clear_database, name='clear_database'),
    path(r'progress-bar-upload/', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

