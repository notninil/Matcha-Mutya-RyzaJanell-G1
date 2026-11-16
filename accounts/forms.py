from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


def clean_email(form):
    email = form.cleaned_data["email"].lower()
    if User.objects.filter(email__iexact=email).exclude(pk=form.instance.pk).exists():
        raise forms.ValidationError("This email address is already registered.")
    return email


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already registered.")
        return username

    def clean_email(self):
        return clean_email(self)


