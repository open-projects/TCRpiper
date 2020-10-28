from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

app_name = 'filestorage'
urlpatterns = [
    url(r'', TemplateView.as_view(template_name='home.html'), name='home'),
    #url(r'^filestorage/', include(('filestorage.urls', 'filestorage'), namespace='filestorage')),
    url(r'clear/', views.clear_database, name='clear_database'),
    url(r'basic-upload/', views.BasicUploadView.as_view(), name='basic_upload'),
    url(r'progress-bar-upload/', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'drag-and-drop-upload/', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
