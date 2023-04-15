from django.conf import settings
import os


def from_root(path):
    return os.path.join(settings.BASE_DIR, *path.strip("/").split("/"))
