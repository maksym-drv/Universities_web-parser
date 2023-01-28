from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from .models import Template
from .forms import NewTemplateForm


class MyTemplates(LoginRequiredMixin, ListView):

    model = Template
    template_name = 'my_templates.html'

    def get_queryset(self):
        return Template.objects.filter( user = self.request.user )


class NewTemplate(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'new_template.html'
    success_url = reverse_lazy('my_templates')

    def form_valid(self, form: NewTemplateForm):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class EditTemplate(LoginRequiredMixin, FormView):

    form_class = NewTemplateForm
    template_name = 'edit_template.html'
    success_url = reverse_lazy('my_templates')

    def form_valid(self, form: NewTemplateForm):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EditTemplate, self).get_form_kwargs()
        kwargs['instance'] = Template.objects.get(pk=self.kwargs['pk'])
        return kwargs