from django.db import models  # pylint: disable=import-error
from django.contrib.auth.models import (  # pylint: disable=import-error
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# from django.db.models.expressions import Value


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and save new user
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        # Create and save new superuser
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Custom user model using email instead of username
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    # TODO: Maybe do is_leader instead for bandleader app
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
