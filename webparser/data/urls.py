from django.urls import path
from .views import TaskView

urlpatterns = [
    path('task/<str:id>/', TaskView.as_view(), name='check_task'),
]