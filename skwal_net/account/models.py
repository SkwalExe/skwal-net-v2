from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
    objects = UserManager()
    bio = models.CharField(max_length=256, blank=True, null=True)
    readme = models.TextField(blank=True, null=True, default="# Hello, world!")
    icon_filename = models.CharField(max_length=32, default="default.gif")
    icon_version = models.IntegerField(default=0)
    icon_default = models.BooleanField(default=True)
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
