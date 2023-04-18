from django.shortcuts import render
import os
from django.http import HttpResponse
from main.utils import *


def index(request):
    module = request.GET.get("module", "introduction")
    section = request.GET.get("section", "introduction") + ".md"

    modules = os.listdir(from_root("documents/sections"))
    if module not in modules:
        return HttpResponse("Module not found", status=404)

    sections = os.listdir(from_root("documents/sections/" + module))
    if section not in sections:
        return HttpResponse("Section not found", status=404)

    section_content = open(
        from_root(f"documents/sections/{module}/{section}"), "r").read()
    sidebar_content = open(
        from_root(f"documents/sections/{module}/_sidebar.md"), "r").read()

    return render(request, "docs/index.html", {
        "section_content": section_content,
        "sidebar_content": sidebar_content,
        "page_title": "📜 " + " ".join(module.split("-")).title()
    })
