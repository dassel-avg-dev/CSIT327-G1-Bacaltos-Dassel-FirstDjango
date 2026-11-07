from django.urls import path
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm
from .views import ProfileView, SignUpView

urlpatterns = [
    path("login/", LoginView.as_view(authentication_form=CustomAuthenticationForm), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("signup/", SignUpView.as_view(), name="signup-with-slash"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
