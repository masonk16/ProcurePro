from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model to handle user data with email used as username and first name and last name fields removed.
    """

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True, null=True)
    company_name = models.CharField(max_length=200, null=True)
    address = models.TextField(max_length=200, null=True)
    industry = models.CharField(null=True, max_length=100)
    phone_number = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)
    user_type = models.CharField(max_length=20, null=True)
    date_joined = models.DateTimeField(verbose_name="date_joined", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "company_name",
        "address",
        "industry",
        "phone_number",
        "website",
        "user_type",
    ]

    objects = UserManager()

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return self.email


class Supplier(models.Model):
    supplier = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.supplier.email


class Contractor(models.Model):
    contractor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="contractor",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.contractor.email


class Tender(models.Model):
    """
    Model for handling Tender data.
    """

    CATEGORY_CHOICES = (
        ("Advertising", "Advertising"),
        ("Agriculture", "Agriculture"),
        ("Chemicals", "Chemicals"),
        ("Construction", "Construction"),
        ("Economics", "Economics"),
        ("Education", "Education"),
        ("Energy", "Energy"),
        ("Engineering", "Engineering"),
        ("Finance", "Finance"),
        ("Food", "Food"),
        ("Forestry", "Forestry"),
        ("Goods", "Goods"),
        ("Healthcare", "Healthcare"),
        ("Infrastructure", "Infrastructure"),
        ("Manufacturing", "Manufacturing"),
        ("Market Research", "Market Research"),
        ("Mining", "Mining"),
        ("Pharmaceuticals", "Pharmaceuticals"),
        ("Production", "Production"),
        ("Real Estate", "Real Estate"),
        ("Research", "Research"),
        ("Retail", "Retail"),
        ("Telecommunications", "Telecommunications"),
    )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200, null=True)
    notice_number = models.CharField(max_length=200, null=True)
    tender_name = models.CharField(max_length=200, null=True)
    requirement_details = models.TextField(null=True)
    budget = models.IntegerField(null=True)
    deadline = models.DateTimeField(null=True)
    opening_date = models.DateTimeField(verbose_name="opening_date", auto_now_add=True)
    owner = models.CharField(default=None, null=True, max_length=200)

    def __str__(self):
        return str(self.id)


class Bids(models.Model):
    """
    Model for handling Bid data.
    """

    description = models.TextField(null=True)
    bid_price = models.IntegerField(null=True)
    submission_date = models.DateTimeField(
        verbose_name="submission_date", auto_now_add=True
    )
    tender_id = models.ForeignKey(
        Tender, default=None, related_name="bids", null=True, on_delete=models.CASCADE
    )
    owner = models.CharField(default=None, null=True, max_length=200)

    def __str__(self):
        return str(self.id)
