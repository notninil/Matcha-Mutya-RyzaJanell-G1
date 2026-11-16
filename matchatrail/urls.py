from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

from accounts.views import RoleLoginView, dashboard, explorer_dashboard, owner_dashboard, profile, register

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard")),
    path("register/", register, name="register"),
    path("login/", RoleLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/explorer/", explorer_dashboard, name="explorer_dashboard"),
    path("dashboard/owner/", owner_dashboard, name="owner_dashboard"),
]
