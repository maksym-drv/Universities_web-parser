from django.contrib.auth.mixins import LoginRequiredMixin
from webparser.data.tasks import info_task, regions_task
from webparser.options.models import University
from django.views.generic import ListView, \
    FormView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .forms import TemplateForm
from .models import Template

class InfoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template = Template.objects.get(pk = self.kwargs.get('pk'))
        
        task = info_task.delay(
            specialities = [speciality.registry_id for speciality in template.speciality.all()],
            unis = list(template.university.values_list('registry_id', flat=True)),
            year = template.year,
            qualification = template.qualification.registry_id,
            education_base = template.education_base.registry_id
        )

        context['template'] = template
        context['task'] = task.id
        return context


class TemplatesView(LoginRequiredMixin, ListView):

    model = Template
    template_name = 'templates.html'

    def get_queryset(self):
        return Template.objects.filter( user = self.request.user )


class NewTemplateView(LoginRequiredMixin, FormView):

    form_class = TemplateForm
    template_name = 'new.html'
    success_url = reverse_lazy('templates')

    def form_valid(self, form: TemplateForm):
        form.instance.user = self.request.user
        form.save()
        unis = self.request.POST.getlist('university')
        for uni in unis:
            uni, created  = University.objects.get_or_create(
                registry_id = uni
            )
            form.instance.university.add(uni)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task = regions_task.delay()

        context['task'] = task.id
        return context


class EditTemplateView(LoginRequiredMixin, FormView):

    form_class = TemplateForm
    template_name = 'edit.html'
    success_url = reverse_lazy('templates')

    def form_valid(self, form: TemplateForm):
        form.instance.user = self.request.user
        form.instance.university.clear()
        unis = self.request.POST.getlist('university')
        for uni in unis:
            uni, created = University.objects.get_or_create(
                registry_id = uni
            )
            form.instance.university.add(uni)
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EditTemplateView, self).get_form_kwargs()
        kwargs['instance'] = Template.objects.get(pk=self.kwargs['pk'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        saved_unis = Template.objects.get(
            pk = self.kwargs['pk']
        ).university.all()

        task = regions_task.delay(
            saved_unis = [uni.registry_id for uni in saved_unis],
        )

        context['task'] = task.id
        return context

class DeleteTemplateView(LoginRequiredMixin, DeleteView):

    model = Template
    success_url = reverse_lazy('templates')
    template_name = 'delete.html'
