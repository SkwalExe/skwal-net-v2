from account.models import *
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from main.classes import *
from account.utils import *
from django.contrib.auth import authenticate
from . import settings_forms


class RegisterForm(UserCreationForm):
    form_name = "Register"
    submit_button = "Register"
    form_links = [
        NavButton("/login", "Login", "fa fa-sign-in-alt"),
    ]
    form_disclaimer = "By creating an account and using our services, you agree to our <a href='/tos'>Terms of Service 📜</a> and <a href='/privacy'>Privacy Policy 🔒</a>."

    class Meta:
        model = User
        fields = ["username", "email",
                  "display_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "_Username92",
            "email": "name@example.com",
            "password1": "Your password",
            "password2": "Confirm password",
            "display_name": "Display Name"
        }

        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = placeholders[field]

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False

        ok = True

        # check if the username is already taken
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            self.add_error("username", "Username is already in use")
            ok = False

        # check if the email is already taken
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            self.add_error("email", "Email is already in use")
            ok = False

        # Check if the username is valid
        if not is_valid_username(self.cleaned_data["username"]):
            self.add_error(
                "username", "Username must contain at least one letter or number, and can include dashes, dots, and underscores")
            ok = False

        return ok


class LoginForm(ModelForm):
    form_name = "Login"
    submit_button = "Login"
    form_links = [
        NavButton("/register", "Register", "fa fa-user-plus"),
        NavButton("/settings/password/", "Reset Password", "fa fa-key")
    ]

    class Meta:
        model = User
        fields = ["email", "password"]
        widgets = {
            "password": PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "email": "name@example.com",
            "password": "Your password",
        }
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = placeholders[field]

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                self.add_error(None, "Invalid email or password")
            else:
                cleaned_data["user"] = user

        return cleaned_data
