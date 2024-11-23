from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("plan_list")
        messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})
