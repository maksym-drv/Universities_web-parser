from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DeleteView, TemplateView
from .models import Template, Report
from options.models import Region
from .forms import NewTemplateForm, ReportForm
from multiprocessing.dummy import Pool
from .parsing import Parser
from .scraping import Scraper
from requests import get
from django.conf import settings
from options.models import University

from django.http import JsonResponse

from json import dump
from time import time

def my_ajax_view(request, pk: int):

    template = Template.objects.get(pk = pk)

    start = time()
    
    parser = Scraper(
        unis = list(template.university.values_list('registry_id', flat=True)),
        url = settings.TARGET_URL,
        executable_path = settings.EXECUTABLE_PATH,
        firefox_options = settings.FIREFOX_OPTIONS,
        qualification = template.qualification.registry_id,
        education_base = template.education_base.registry_id
    )

    specialities = [speciality.registry_id for 
                    speciality in template.speciality.all()]

    with Pool(len(specialities)) as p:
        spec_unis = p.map(parser.get_uni_data, specialities)

    unis = []

    for spec_uni in spec_unis:
        for uni in spec_uni:
            uni_index = next((index for (index, _uni) in enumerate(unis) 
                            if _uni['id'] == uni['id']), None)
            
            if isinstance(uni_index, int):
                unis[uni_index]['offers'] += uni['offers']
            else:
                _uni = {}
                _uni['id'] = uni['id']
                _uni['name'] = uni['name']
                _uni['offers'] = []
                _uni['offers'] += uni['offers']
                unis.append(_uni)

    response = get(settings.UNIVERSITIES_URL, 
                    params=settings.DEFAULT_PARAMS)
    all_unis: list = response.json()
    
    regions = []
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


    with open('data.json', 'w') as file:
        dump(regions, file, ensure_ascii=False)

    print(f'PARSING TIME ==> {time() - start}')

    data = {}
    data['regions'] = regions

    return JsonResponse(data)

class TemplateDataView(LoginRequiredMixin, TemplateView):

    template_name = 'template_data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['template_data'] = self.kwargs.get('pk')
        
        return context


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