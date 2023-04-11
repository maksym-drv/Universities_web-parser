from django.urls import path
from .views import TemplatesView, NewTemplateView, EditTemplateView, \
                ReportView, DeleteTemplateView, DownloadReportView, InfoTemplateView, \
                check_parse


urlpatterns = [
    path('templates/', TemplatesView.as_view(), name='templates'),
    path('info/<int:pk>/', InfoTemplateView.as_view(), name='info_template'),
    path('new/', NewTemplateView.as_view(), name='new_template'),
    path('edit/<int:pk>/', EditTemplateView.as_view(), name='edit_template'),
    # path('report/<int:pk>/', ReportView.as_view(), name='report'),
    path('delete_template/<int:pk>/', DeleteTemplateView.as_view(), name='delete_template'),
    #path('download_report/<int:pk>/', DownloadReportView.as_view(), name='download_report'),
    #path('parse/<int:pk>/', parse_info, name='parse'),
    path('check/<str:task_id>/', check_parse, name='check'),
]