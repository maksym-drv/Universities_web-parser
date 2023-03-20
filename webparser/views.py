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


class MyTemplatesView(LoginRequiredMixin, ListView):

    model = Template
    template_name = 'my_templates.html'

    def get_queryset(self):
        return Template.objects.filter( user = self.request.user )


class NewTemplateView(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'new_template.html'
    success_url = reverse_lazy('my_templates')

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

        params = {
            'ut': 1,
            'exp': 'json'
        }

        response = get(settings.UNIVERSITIES_URL, params=params)
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
    template_name = 'edit_template.html'
    success_url = reverse_lazy('my_templates')

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
    success_url = reverse_lazy('my_templates')
    template_name = 'delete_template.html'


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