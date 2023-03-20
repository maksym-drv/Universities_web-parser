from django.urls import path
from .views import MyTemplatesView, NewTemplateView, EditTemplateView, \
                ReportView, DeleteTemplateView, DownloadReportView


urlpatterns = [
    path('my_templates/', MyTemplatesView.as_view(), name='my_templates'),
    path('new_template/', NewTemplateView.as_view(), name='new_template'),
    path('edit_template/<int:pk>/', EditTemplateView.as_view(), name='edit_template'),
    path('report/<int:pk>/', ReportView.as_view(), name='report'),
    path('delete_template/<int:pk>/', DeleteTemplateView.as_view(), name='delete_template'),
    path('download_report/<int:pk>/', DownloadReportView.as_view(), name='download_report'),
]