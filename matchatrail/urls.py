from django.urls import path
from django.views.generic import RedirectView

from accounts.views import register

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="register")),
    path("register/", register, name="register"),
]
