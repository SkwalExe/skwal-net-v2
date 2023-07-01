from django.shortcuts import render
import os
from django.http import HttpResponse
from main.utils import *


def index(request, module="introduction", section="introduction"):
    return render_markdown(request, f"documentation/{module}/", section)


def tos(request):
    return render_markdown(request, "legal", "tos")


def privacy(request):
    return render_markdown(request, "legal", "privacy")


def cookies(request):
    return render_markdown(request, "legal", "cookies")


def credits(request):
    return render(request, "documentation/credits.html", {
        "no_sidebar": True,
        "stylesheets": ["credits"],
    })
