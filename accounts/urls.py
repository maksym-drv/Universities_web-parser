from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, LoginView, ProfileView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('changepassword/', ChangePasswordView.as_view(), name='change_password'),
    path('signup/', SignUpView.as_view(), name='signup'),
]