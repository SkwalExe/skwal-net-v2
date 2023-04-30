from django.shortcuts import render
from django.http import HttpResponse
from main.classes import *
from main.utils import *


def home(request):
    return render(request, 'main/home.html', {
        "nav_buttons": [
            HomeNavButton(),
            AccountNavButton()
            if request.user.is_authenticated else
            LoginNavButton()
        ]
    })
