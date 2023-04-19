from django.conf import settings
import os
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render


def from_root(path):
    return os.path.join(settings.BASE_DIR, *path.strip("/").split("/"))


def rediverse(*args, **kwargs):
    return redirect(reverse(*args, **kwargs))


def error_page(request, code=None, message=None):
    return render(request, 'error.html', {
        "error_code": code,
        "error_message": message,
        "small_body": True,
        "no_sidebar": True,
    })
