from django.urls import path
from .views import check_info, check_regions


urlpatterns = [
    path('check/<str:id>/', check_info, name='data_check'),
    path('check-regions/<str:id>/', check_regions, name='regions_check'),
]