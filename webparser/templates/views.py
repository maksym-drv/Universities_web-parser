from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DeleteView, TemplateView

from .models import Template
from .forms import NewTemplateForm
from webparser.data.tasks import parser_task
from webparser.data.scraping import Scraper
from webparser.options.models import University, Region

class InfoTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        template = Template.objects.get(pk = self.kwargs.get('pk'))
        
        task = parser_task.delay(
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
        for uni in unis:
            uni, created  = University.objects.get_or_create(
                registry_id = uni
            )
            form.instance.university.add(uni)
        # report = Report(template = form.instance)
        # report.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        regions = []
    
        for region in Region.objects.all():

            _region = {}
            _region['id'] = region.id
            _region['name'] = region.name

            params: dict = settings.DEFAULT_PARAMS.copy()
            params['lc'] = region.registry_id

            unis: list = Scraper.get_json(
                settings.UNIVERSITIES_URL, 
                params=params
            )

            _region['unis'] = unis

            if _region['unis']:
                regions.append(_region)

        context['regions'] = regions
        return context


class EditTemplateView(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'edit.html'
    success_url = reverse_lazy('templates')

    def form_valid(self, form: NewTemplateForm):
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

        regions = []
    
        for region in Region.objects.all():

            _region = {}
            _region['id'] = region.id
            _region['name'] = region.name

            params: dict = settings.DEFAULT_PARAMS.copy()
            params['lc'] = region.registry_id

            unis: list = Scraper.get_json(
                settings.UNIVERSITIES_URL, 
                params=params
            )

            saved_unis = Template.objects.get(
                pk = self.kwargs['pk']
            ).university.all()
            
            for uni in unis:
                if saved_unis.filter(registry_id = uni['university_id']).exists():
                    uni['checkbox_value'] = True

            _region['unis'] = unis

            if _region['unis']:
                regions.append(_region)

        context['regions'] = regions
        return context


class DeleteTemplateView(LoginRequiredMixin, DeleteView):

    model = Template
    success_url = reverse_lazy('templates')
    template_name = 'delete.html'


## class ReportView(LoginRequiredMixin, FormView):
## 
##     form_class = ReportForm
##     template_name = 'report.html'
## 
##     def form_valid(self, form: NewTemplateForm):
##         form.save()
##         self.success_url = reverse_lazy('download_report', kwargs={'pk': self.kwargs['pk']})
##         return super().form_valid(form)
## 
##     def get_form_kwargs(self):
##         kwargs = super(ReportView, self).get_form_kwargs()
##         kwargs['instance'] = Report.objects.get(pk=self.kwargs['pk'])
##         return kwargs
## 
## 
## class DownloadReportView(LoginRequiredMixin, TemplateView):
## 
##     template_name = 'download_report.html'
## 
##     def get(self, request, pk: int):
## 
##         report = Report.objects.get(pk=pk)
##         options: Template = report.template
## 
##         parser = Parser(
##             qualification   = options.qualification,
##             education_base  = options.education_base,
##             speciality      = options.speciality,
##             region          = options.region,
##             education_form  = options.education_form,
##             course          = options.course,
##             university      = options.university,
##             study_program   = options.study_program,
##         )
## 
##         for name in parser.names:
##             print('name ==> ', name) 
## 
##         context = {}
##         context['data'] = parser.names
##         return self.render_to_response(context)