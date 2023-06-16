from django.conf import settings
import os
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from main.classes import *
from django.core.mail import send_mail as _send_mail
from django.template.loader import render_to_string
import random
import string


def send_mail(recipient, object, template, args = {}, fail_silently=False):
    msg_plain = render_to_string(f"email/{template}.txt", {**args,"object": object})
    msg_html = render_to_string(f"email/{template}.html", {**args,"object": object})
    return _send_mail(
        object, 
        msg_plain,
        settings.DEFAULT_FROM_EMAIL, 
        [recipient],
        fail_silently=fail_silently,
        html_message=msg_html
    )

def from_root(path):
    return os.path.join(settings.BASE_DIR, *path.strip("/").split("/"))


def rediverse(*args, **kwargs):
    """Short for redirect(reverse(...))"""
    return redirect(reverse(*args, **kwargs))


def error_page(request, message=None, code=None):
    """Render an error page with the given code and message"""
    return render(request, 'error.html', {
        "error_code": code,
        "error_message": message,
        "small_body": True,
        "no_sidebar": True,
    }, status=code if type(code) == int else 500)


def render_markdown(request, dir, body="introduction", sidebar="_sidebar"):
    """Render a page showing the given markdown file in the given directory"""
    body += ".md"
    sidebar += ".md"

    # Prevent directory traversal :
    # Check if the given markdown file is the /md_docs directory
    # or a subdirectory of it
    dir_to_check = from_root("md_docs")
    for dir_name in dir.strip("/").split("/"):
        subdirs = os.listdir(dir_to_check)
        if dir_name not in subdirs:
            return error_page(request, "Document not found", 404)
        dir_to_check = os.path.join(dir_to_check, dir_name)
    dir = dir_to_check
    for file_name in [body, sidebar]:
        if file_name not in os.listdir(dir):
            return error_page(request, "Document not found", 404)
    sidebar_content = open(f"{dir}/{sidebar}", "r").read()
    body_content = open(f"{dir}/{body}", "r").read()

    return render(request, "markdown.html", {
        "sidebar_content": sidebar_content,
        "body_content": body_content,
        "page_title": "📜 " + " ".join(body[:-3].split("-")).title()
    })


def render_form(request, form):
    return render(request, "form.html", {
        "form": form,
        "page_title": form.form_name or "Form",
        "no_sidebar": True,
        "small_body": True,
        "nav_buttons": form.nav_buttons or [HomeNavButton()],
    })


def generate_token():
    """Generate a random 32-character token"""
    return ''.join(random.choices(string.hexdigits, k=32))