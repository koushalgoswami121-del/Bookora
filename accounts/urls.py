from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("pricing/", views.pricing, name="pricing"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("@<str:username>/", views.profile_view, name="profile"),
]
