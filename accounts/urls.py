from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUp, Profile, Login

urlpatterns = [
    path('login/', Login.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('signup/', SignUp.as_view(), name='signup')
]