from django.urls import path
from .views import check_parse


urlpatterns = [
    path('check/<str:id>/', check_parse, name='data_check'),
]