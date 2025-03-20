from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from applications.common import models as base_models

# from django.db.models.signals import post_save
# from django.dispatch import receiver


class UserManager(base_models.BaseManager, BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with given email and password
        """
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.account_type = User.AccountType.PLATFORM_ADMIN
        user.save(using=self._db)

        return user


class User(PermissionsMixin, base_models.BaseModel, AbstractBaseUser):
    """Default user for api_project."""

    class AccountType(models.TextChoices):
        ADMIN = "admin", _("Admin")

    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    first_name = models.CharField(_("First Name"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name"), blank=True, max_length=255)
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        help_text="Contact phone number",
    )
    account_type = models.CharField(
        _("Account Type"),
        max_length=100,
        choices=AccountType.choices,
        default=AccountType.ADMIN,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" or self.email

    def get_short_name(self):
        return self.first_name or self.email

    def __str__(self) -> str:
        return self.get_full_name() or self.email


# class Profile(base_models.BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
#     display_name = models.CharField(max_length=50, null=True, blank=True)
#     profile_image = models.ImageField(upload_to="profiles", null=True, blank=True)
#     country = models.CharField(max_length=50, null=True, blank=True)
#     phone_number = PhoneNumberField(
#         unique=True,
#         blank=True,
#         null=True,
#         help_text="+999999999",
#     )

#     def __str__(self):
#         return f"{self.user.email}"


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
