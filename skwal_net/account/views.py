from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from main.classes import *
from .forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_(request):
    if request.user.is_authenticated:
        return redirect(reverse("account"))

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session["session_date"] = datetime.datetime.now(
            ).timestamp()
            return redirect(reverse("account"))

    else:
        form = RegisterForm()

    return render(request, "form.html", {
        "form": form,
        "page_title": "Register",
        "no_sidebar": True,
        "small_body": True,
        "nav_buttons": [HomeNavButton(), NavButton("/login", "Login", "fa fa-sign-in-alt")],
    })


def login_(request):
    if request.user.is_authenticated:
        return redirect(reverse("account"))

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request, email=form.cleaned_data["email"], password=form.cleaned_data["password"])

            if user is not None:
                login(request, user)
                request.session["session_date"] = datetime.datetime.now(
                ).timestamp()
                return redirect(reverse("account"))
            else:
                form.add_error(None, "Invalid email or password")

    else:
        form = LoginForm()

    return render(request, "form.html", {
        "form": form,
        "page_title": "Login",
        "no_sidebar": True,
        "small_body": True,
        "nav_buttons": [HomeNavButton(), NavButton("/register", "Register", "fa fa-sign-in-alt")],
    })


def account_(request):
    return HttpResponse(f"You'fe logged in : {request.user}", status=200)
