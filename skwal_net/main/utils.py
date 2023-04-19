from django.conf import settings
import os
from django.shortcuts import redirect
from django.urls import reverse


def from_root(path):
    return os.path.join(settings.BASE_DIR, *path.strip("/").split("/"))


def rediverse(*args, **kwargs):
    return redirect(reverse(*args, **kwargs))
