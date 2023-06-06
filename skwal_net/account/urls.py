from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_, name="register"),
    path("login/", views.login_, name="login"),
    path("profile/", views.profile_, name="profile"),
    path("profile/@<str:username>/", views.profile_, name="profile"),
    path("logout/", views.logout_, name="logout"),
    path("settings/", views.settings_, name="settings"),
]
