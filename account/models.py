from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.db import models

username_validator = UnicodeUsernameValidator()


class Account(AbstractUser):

    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        unique=True,
        null=False,
        blank=False
    )
    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(
        _("first name"),
        max_length=60,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        _("last name"),
        max_length=60,
        blank=False,
        null=False
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        null=False,
        unique=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        auto_now_add=True
    )

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)
