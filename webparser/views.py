from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DeleteView, TemplateView
from .models import Template, Report
from options.models import Region
from .forms import NewTemplateForm, ReportForm
from .parsing import Parser
from requests import get
from django.conf import settings
from options.models import University
from django.http import JsonResponse
from celery.result import AsyncResult
from .tasks import create_task

def check_parse(request, task_id: str):

    # check the task status
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS':
        
        # the task is complete, return the result
        unis = task.result
        regions = []

        response = get(settings.UNIVERSITIES_URL, 
                    params=settings.DEFAULT_PARAMS)
        all_unis: list = response.json()
        
        for uni in unis:
            
            region_name = next((_uni['region_name_u'] for _uni in all_unis 
                        if _uni['university_id'] == uni['id']), None)
            
            region_index = next((index for (index, _region) in enumerate(regions) 
                    if _region['name'] == region_name), None)
            
            if isinstance(region_index, int):
                regions[region_index]['unis'].append(uni)
            else:
                _region = {}
                _region['id'] = Region.objects.get(name = region_name).registry_id
                _region['name'] = region_name
                _region['unis'] = []
                _region['unis'].append(uni)
                regions.append(_region)

        return JsonResponse({'status': 'SUCCESS', 'result': regions})
    elif task.state == 'PENDING' or task.state == 'STARTED':
        # the task is still running
        return JsonResponse({'status': task.state})
    else:
        # the task failed
        return JsonResponse({'status': 'FAILURE', 'result': task.result})

class InfoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template = Template.objects.get(pk = self.kwargs.get('pk'))
        
        task = create_task.delay(
            specialities = [speciality.registry_id for speciality in template.speciality.all()],
            unis = list(template.university.values_list('registry_id', flat=True)),
            qualification = template.qualification.registry_id,
            education_base = template.education_base.registry_id
        )

        context['task_id'] = task.id
        return context


class TemplatesView(LoginRequiredMixin, ListView):

    model = Template
    template_name = 'templates.html'

    def get_queryset(self):
        return Template.objects.filter( user = self.request.user )


class NewTemplateView(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'new.html'
    success_url = reverse_lazy('templates')

    def form_valid(self, form: NewTemplateForm):
        form.instance.user = self.request.user
        form.save()
        unis = self.request.POST.getlist('university')
        if unis:
            for uni in unis:
                uni, created  = University.objects.get_or_create(
                    registry_id = uni
                )
                form.instance.university.add(uni)
        report = Report(template = form.instance)
        report.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        response = get(settings.UNIVERSITIES_URL, 
                       params=settings.DEFAULT_PARAMS)
        unis: list = response.json()
        data = {}

        for uni in unis:
            
            uni: dict
            region = uni.pop('region_name_u')
            region = Region.objects.get(name = region)

            if not data.get(region.registry_id):
                data[region.registry_id] = {}
                data[region.registry_id]['name'] = region.name
                data[region.registry_id]['unis'] = []
                data[region.registry_id]['unis'].append(uni)
            else: data[region.registry_id]['unis'].append(uni)
        
        context['regions'] = data
        return context


class EditTemplateView(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'edit.html'
    success_url = reverse_lazy('templates')

    def form_valid(self, form: NewTemplateForm):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EditTemplateView, self).get_form_kwargs()
        kwargs['instance'] = Template.objects.get(pk=self.kwargs['pk'])
        return kwargs


class DeleteTemplateView(LoginRequiredMixin, DeleteView):

    model = Template
    success_url = reverse_lazy('templates')
    template_name = 'delete.html'


class ReportView(LoginRequiredMixin, FormView):

    form_class = ReportForm
    template_name = 'report.html'

    def form_valid(self, form: NewTemplateForm):
        form.save()
        self.success_url = reverse_lazy('download_report', kwargs={'pk': self.kwargs['pk']})
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ReportView, self).get_form_kwargs()
        kwargs['instance'] = Report.objects.get(pk=self.kwargs['pk'])
        return kwargs


class DownloadReportView(LoginRequiredMixin, TemplateView):

    template_name = 'download_report.html'

    def get(self, request, pk: int):

        report = Report.objects.get(pk=pk)
        options: Template = report.template

        parser = Parser(
            qualification   = options.qualification,
            education_base  = options.education_base,
            speciality      = options.speciality,
            region          = options.region,
            education_form  = options.education_form,
            course          = options.course,
            university      = options.university,
            study_program   = options.study_program,
        )

        for name in parser.names:
            print('name ==> ', name) 

        context = {}
        context['data'] = parser.names
        return self.render_to_response(context)