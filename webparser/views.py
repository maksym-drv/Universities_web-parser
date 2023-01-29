from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from .models import Template, Report
from .forms import NewTemplateForm, ReportForm


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
        report = Report(template = form.instance)
        report.save()
        return super().form_valid(form)


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


class ReportView(LoginRequiredMixin, FormView):

    form_class = ReportForm
    template_name = 'report.html'
    success_url = reverse_lazy('my_templates')

    def form_valid(self, form: NewTemplateForm):
        #form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ReportView, self).get_form_kwargs()
        kwargs['instance'] = Report.objects.get(pk=self.kwargs['pk'])
        return kwargs