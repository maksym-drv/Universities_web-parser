from django.urls import path
from .views import TemplatesView, NewTemplateView, EditTemplateView, \
                DeleteTemplateView, InfoTemplateView


urlpatterns = [
    path('', TemplatesView.as_view(), name='templates'),
    path('info/<int:pk>/', InfoTemplateView.as_view(), name='templates_info'),
    path('new/', NewTemplateView.as_view(), name='templates_new'),
    path('edit/<int:pk>/', EditTemplateView.as_view(), name='templates_edit'),
    path('delete/<int:pk>/', DeleteTemplateView.as_view(), name='templates_delete'),
]