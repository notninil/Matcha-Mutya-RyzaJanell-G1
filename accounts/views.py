from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError as error:
            field = {
                "accounts_email_ci_unique": "email",
                "accounts_username_ci_unique": "username",
                "accounts_user_username_key": "username",
            }.get(error.__cause__.diag.constraint_name)
            if field is None:
                raise
            form.add_error(field, f"This {field} is already registered.")
        else:
            messages.success(request, "Your Explorer account was created.")
            return redirect("register")
    return render(request, "form.html", {"form": form, "title": "Create an Explorer account"})
