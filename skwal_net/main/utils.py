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


def render_markdown(request, dir, body="introduction", sidebar="_sidebar"):
    body += ".md"
    sidebar += ".md"

    dir_to_check = from_root("md_docs")
    for dir_name in dir.strip("/").split("/"):
        subdirs = os.listdir(dir_to_check)
        if dir_name not in subdirs:
            return error_page(request, "404", "Document not found")
        dir_to_check = os.path.join(dir_to_check, dir_name)
    dir = dir_to_check
    print(os.listdir(dir))
    for file_name in [body, sidebar]:
        if file_name not in os.listdir(dir):
            return error_page(request, "404", "Document not found")
    print("ok")
    sidebar_content = open(f"{dir}/{sidebar}", "r").read()
    body_content = open(f"{dir}/{body}", "r").read()

    return render(request, "markdown.html", {
        "sidebar_content": sidebar_content,
        "body_content": body_content,
        "page_title": "📜 " + " ".join(body[:-3].split("-")).title()
    })
