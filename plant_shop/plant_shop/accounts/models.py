from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from plant_shop.utils.validators import validate_alphabet_characters


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class AppUser(auth_models.AbstractBaseUser, PermissionsMixin):
    FIRST_NAME_MAX_LEN = 50
    FIRST_NAME_MIN_LEN = 3
    LAST_NAME_MAX_LEN = 50
    LAST_NAME_MIN_LEN = 3

    username = None

    email = models.EmailField(max_length=50, unique=True, validators=())

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            validate_alphabet_characters,
        ),
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            validate_alphabet_characters,
        ),
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User account"


class UserProfile(models.Model):
    ADDRESS_MAX_LEN = 50
    CITY_MAX_NAME_LEN = 30
    ZIP_MAX_LEN = 20

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
    )

    phone_number = models.CharField(
        max_length=50
    )

    address_line_1 = models.CharField(
        blank=True,
        max_length=ADDRESS_MAX_LEN,
    )
    address_line_2 = models.CharField(
        blank=True,
        max_length=ADDRESS_MAX_LEN,
    )
    city = models.CharField(
        blank=True,
        max_length=CITY_MAX_NAME_LEN
    )
    zip_code = models.CharField(
        blank=True,
        max_length=ZIP_MAX_LEN,
    )

    @receiver(post_save, sender=AppUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @property
    def profile_email(self):
        return self.user.email

    @property
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "User profile"
