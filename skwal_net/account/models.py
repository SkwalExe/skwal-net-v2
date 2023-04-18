from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    AbscactBaseUser already provides the following fields:
     - password
     - last_login
     - is_active
    """

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=32, blank=True, null=True)

    objects = UserManager()
