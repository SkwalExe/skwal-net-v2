from django.shortcuts import render
from django.http import HttpResponse
from main.classes import *
from main.utils import *
from .forms import *
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.themes import themes

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

settings_forms = {
    "theme": {
        "form": settings_forms.ThemeChangeForm,
        "icon": "fa fa-palette",
        "model_form": True,
        "visible": True
    },
    "usernames": {
        "form": settings_forms.NewUsernamesForm,
        "icon": "fa fa-user",
        "model_form": True,
        "visible": True
    },
    "email": {
        "form": settings_forms.SendEmailChangeLinkForm,
        "icon": "fa fa-envelope",
        "model_form": True,
        "visible": True
    },
    "password": {
        "form": settings_forms.SendPasswordResetLinkForm,
        "icon": "fa fa-key",
        "model_form": False,
        "visible": True,
        "no_login_required": True,
    },
    "logout_sessions": {
        "form": settings_forms.LogoutSessionsForm,
        "icon": "fa fa-sign-out-alt",
        "model_form": False,
        "visible": True
    },
    "delete": {
        "form": settings_forms.SendAccountDeletionLinkForm,
        "icon": "fa fa-trash",
        "model_form": False,
        "visible": True
    },
    "_email": {
        "form": settings_forms.ChangeEmailForm,
        "model_form": True,
        "visible": False
    },
    "_password": {
        "form": settings_forms.ChangePasswordForm,
        "model_form": True,
        "visible": False
    },
    "_delete": {
        "form": settings_forms.DeleteAccountForm,
        "model_form": False,
        "visible": False
    },
}


def settings_(request, section=None):
    # Check if section exists
    if section not in settings_forms:
        return rediverse("settings", args=["usernames"])

    # Get the corresponding setting object
    setting = settings_forms[section]

    # Only allow logged in users to access settings that doesn't have the "no_login_required" property
    if "no_login_required" in setting and not setting["no_login_required"] and not request.user.is_authenticated:
        return rediverse("login")

    # Parse POST data if any; otherwise, create a new forms
    if setting["model_form"] and request.user.is_authenticated:
        form = setting["form"](request.POST or None, instance=request.user)
    else:
        form =  setting["form"](request.POST or None)


    # Check token
    match section:
        case "_email":
            if not request.user.validate_email_change_token(request.GET.get("token")):
                return error_page(request, "Invalid email change token.", 400)

        case "_password":
            user = User.objects.filter(id=request.GET.get("id")).first()
            if user is None or not user.validate_password_reset_token(request.GET.get("token")):
                return error_page(request, "Invalid password reset token.", 400)

        case "_delete":
            if not request.user.validate_account_deletion_token(request.GET.get("token")):
                return error_page(request, "Invalid account deletion token.", 400)

    # Do changes if POST request
    if request.method == "POST":
        match section:
            case "_email":
                if form.is_valid():
                    form.save()
                    user.new_email_change_token()
                    user.logout_sessions()
                    return rediverse("profile", args=[user.username])
            case "_password":
                if form.is_valid():
                    form.save()
                    user.new_password_reset_token()
                    user.logout_sessions()
                    return rediverse("profile", args=[user.username])
            case "_delete":
                user.delete()
                return rediverse("home")
            case "usernames":
                if setting["model_form"]:
                    form = setting["form"](request.POST, instance=request.user)
                else:
                    form = setting["form"](request.POST)
                if form.is_valid():
                    form.save()
                    return rediverse("profile", args=[request.user.username])
            case "email":
                request.user.send_email_change_link()
                return rediverse("profile", args=[request.user.username])
            case "password":
                request.user.send_password_reset_link()
                return rediverse("profile", args=[request.user.username])
            case "delete":
                request.user.send_account_deletion_link()
                return rediverse("profile", args=[request.user.username])
            case "theme":
                if form.is_valid():
                    form.save()
                else:
                    form.add_error(None, "Invalid theme")
                    # Remove other errors
                    form.errors.pop("theme", None)
            case "logout_sessions":
                request.user.logout_sessions()

    # Render form
    return render(request, "account/settings_base.html", {
        "inverse_sidebar": True,
        "headers": [Header("Settings")],
        "option_list": OptionList(
            [
                [
                    item[0],
                    item[1]["form"].form_name,
                    reverse("settings", args=[item[0]]),
                    item[1]["icon"]
                ] for item in settings_forms.items() if item[1]["visible"]
            ], section),
        "form": form,
        "small_body": True,
        "scripts": ["theme_preview"] if section == "theme" else [],
    })