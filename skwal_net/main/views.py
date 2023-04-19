from django.shortcuts import render
from django.http import HttpResponse
from main.classes import *
from main.utils import *


def home(request):
    return render(request, 'main/home.html', {
        "nav_buttons": [
            NavButton("/", "Home", "fa fa-home"),
            NavButton("/account", "Account", "fa fa-user")
            if request.user.is_authenticated else
            NavButton("/login", "Login", "fa fa-sign-in-alt")
        ]
    })
