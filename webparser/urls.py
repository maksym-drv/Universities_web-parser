from django.urls import path
from .views import MyTemplates


urlpatterns = [
    path('my_templates/', MyTemplates.as_view(), name='my_templates'),
]