from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from main.utils import send_mail, generate_token
from datetime import datetime
from main.themes import themes
from django.contrib.auth.signals import user_logged_in

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_staffuser(
            username,
            email,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=32, unique=True)
    display_name = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(unique=True)
    email_change_token = models.CharField(max_length=64, null=True)
    password_reset_token = models.CharField(max_length=64, null=True)
    account_deletion_token = models.CharField(max_length=64, null=True)
    email_change_token_date = models.DateTimeField(null=True)
    password_reset_token_date = models.DateTimeField(null=True)
    account_deletion_token_date = models.DateTimeField(null=True)
    objects = UserManager()
    bio = models.CharField(max_length=256, blank=True, default="Hello, world!")
    readme = models.TextField(blank=True, default="# Hello, world!")
    icon_filename = models.CharField(max_length=32, default="default.gif")
    icon_version = models.IntegerField(default=0)
    icon_default = models.BooleanField(default=True)
    force_logout_date = models.IntegerField(null=True)
    theme = models.CharField(max_length=32, default="default", choices=[(theme, themes[theme]["name"]) for theme in themes])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __str__(self):
        return self.display_name or self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def icon(self):
        return f"/media/icons/{self.icon_filename}?v={self.icon_version}"

    def send_mail(self, object, template, args, fail_silently=False):
        return send_mail(self.email, object, template, args, fail_silently=fail_silently)

    def send_email_change_link(self):
        self.new_email_change_token()
        return self.send_mail("Change your email address", "email_change_link", {"user": self, "url": f"https://skwal.net/settings/_email?token={self.email_change_token}"})

    def send_password_reset_link(self):
        self.new_password_reset_token()
        return self.send_mail("Reset your password", "password_reset_link", {"user": self, "url": f"https://skwal.net/settings/_password?token={self.password_reset_token}&id={self.id}"})

    def send_account_deletion_link(self):
        self.new_account_deletion_token()
        return self.send_mail("Delete your account", "account_deletion_link", {"user": self, "url": f"https://skwal.net/settings/_delete?token={self.account_deletion_token}"})

    def new_account_deletion_token(self):
        self.account_deletion_token = generate_token()
        self.account_deletion_token_date = datetime.now()
        self.save()
        return self.account_deletion_token

    def new_email_change_token(self):
        self.email_change_token = generate_token()
        self.email_change_token_date = datetime.now()
        self.save()
        return self.email_change_token

    def new_password_reset_token(self):
        self.password_reset_token = generate_token()
        self.password_reset_token_date = datetime.now()
        self.save()
        return self.password_reset_token

    def validate_email_change_token(self, token):
        return self.email_change_token == token and (datetime.now() - self.email_change_token_date).seconds < 1800

    def validate_password_reset_token(self, token):
        return self.password_reset_token == token and (datetime.now() - self.password_reset_token_date).seconds < 1800

    def validate_account_deletion_token(self, token):
        return self.account_deletion_token == token and (datetime.now() - self.account_deletion_token_date).seconds < 1800

    def logout_sessions(self):
        self.force_logout_date = int(round(datetime.now().timestamp()))
        self.save()

def update_session_last_login(sender, user, request, **kwargs):
    if request:
        request.session['LAST_LOGIN_DATE'] = int(round(datetime.now().timestamp()))

user_logged_in.connect(update_session_last_login)
