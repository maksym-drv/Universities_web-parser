from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Template


class MyTemplates(LoginRequiredMixin, ListView):

    model = Template
    template_name = 'templates.html'

    def get_queryset(self):
        return Template.objects.filter( user = self.request.user )