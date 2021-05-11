from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """
    email = models.EmailField(_('email address'), max_length=40, unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    avatars = models.ImageField(_('avatars/'), blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        middle_name = f" {self.middle_name} " if self.middle_name else ' '
        full_name = f"{self.first_name}{middle_name}{self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """

        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """

        send_mail(subject, message, from_email, [self.email], **kwargs)
