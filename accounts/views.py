from .forms import SignUpForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


class Profile(SuccessMessageMixin, LoginRequiredMixin, FormView):

    form_class = UserProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Data was successfully changed'

    def form_valid(self, form):
        form.save()
        #messages.success(self.request, 'Data was successfully changed')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


class Login(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


class SignUp(CreateView):

    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)