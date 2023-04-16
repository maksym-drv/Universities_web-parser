from .forms import SignUpForm, UserProfileForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, FormView):

    form_class = UserProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    success_message = 'Data was successfully changed'

    def form_valid(self, form: UserProfileForm):
        form.save()
        #messages.success(self.request, 'Data was successfully changed')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


class LoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):

    form_class = SignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy('templates_new')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('profile')
    success_message = 'Password changed successfully'

    def form_valid(self, form: ChangePasswordForm):
        
        user = self.request.user
        current_password = form.cleaned_data.get('current_password')
        new_password = form.cleaned_data.get('new_password')
        confirm_new_password = form.cleaned_data.get('confirm_new_password')

        if not user.check_password(current_password):
            form.add_error(None, 'Incorrect current password!')
            return self.form_invalid(form)
        elif new_password != confirm_new_password:
            form.add_error('new_password', 'Passwords do not match!')
            return self.form_invalid(form)
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(self.request, user)
            return super().form_valid(form)
