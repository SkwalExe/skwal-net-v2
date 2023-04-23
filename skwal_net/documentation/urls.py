from django.urls import path
from . import views

urlpatterns = [
    path("docs/", views.index, name="docs_index"),
    path("docs/<str:module>/", views.index, name="docs_module"),
    path("docs/<str:module>/<str:section>/", views.index, name="docs_section"),
    path("tos/", views.tos, name="tos"),
    path("privacy/", views.privacy, name="privacy"),
    path("cookies/", views.cookies, name="cookies"),
    path("credits/", views.credits, name="credits"),
]
