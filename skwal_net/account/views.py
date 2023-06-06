from django.shortcuts import render
from django.http import HttpResponse
from main.classes import *
from main.utils import *
from .forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def logout_(request):
    logout(request)
    return rediverse("home")


def register_(request):
    if request.user.is_authenticated:
        return rediverse("profile", args=[request.user.username])

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            user.display_name = form.cleaned_data["display_name"]
            user.save()
            login(request, user)
            request.session["session_date"] = datetime.datetime.now(
            ).timestamp()
            return rediverse("profile")

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
        return rediverse("profile")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request, email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                request.session["session_date"] = datetime.datetime.now(
                ).timestamp()
                return rediverse("profile")
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


@login_required()
def profile_(request, username=None):
    # If no username is provided, redirect to the current user's profile
    if username is None:
        return rediverse("profile", args=[request.user.username])
    # Try to find the user by username and return a 404 if they don't exist
    user = User.objects.filter(username=username).first()
    if user is None:
        return error_page(request, "The user you are looking for does not exist.", 404)
    return render(request, "account/profile.html", {
        "inverse_sidebar": True,
        "user": user,
        "stylesheets": ["profile-sidebar"],
        "nav_buttons": [HomeNavButton(), LogoutNavButton(), SettingsNavButton()],
    })


@login_required()
def settings_(request):
    return error_page(request, "Settings are not yet implemented", 501)