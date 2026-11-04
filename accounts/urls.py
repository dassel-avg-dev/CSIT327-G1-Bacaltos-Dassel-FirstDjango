from django.urls import path
from .views import ProfileView, SignUpView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("signup/", SignUpView.as_view(), name="signup-with-slash"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
