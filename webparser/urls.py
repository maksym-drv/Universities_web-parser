from django.urls import path
from .views import MyTemplates, NewTemplate, EditTemplate


urlpatterns = [
    path('my_templates/', MyTemplates.as_view(), name='my_templates'),
    path('new_template/', NewTemplate.as_view(), name='new_template'),
    path('edit_template/<int:pk>/', EditTemplate.as_view(), name='edit_template'),
]