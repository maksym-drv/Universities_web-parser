from django.urls import path
from .views import check


urlpatterns = [
    path('check-task/<str:id>/', check, name='check_task'),
]