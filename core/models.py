from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .utils import UserType


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    MANUFACTURING = 'MANU'
    PRODUCTION = 'PRO'
    AGRICULTURE = 'AGR'
    CONSTRUCTION = 'CON'
    RETAIL = 'RT'
    MINING = 'MIN'
    MARKET_RESEARCH = 'MR'
    FINANCE = 'FIN'
    ECONOMICS = 'ECOS'
    EDUCATION = 'EDU'
    CHEMICALS = 'CHEM'
    ADVERTISING = 'ADS'
    GOODS = 'GD'
    REAL_ESTATE = 'RE'
    HEALTHCARE = 'HC'
    FOOD = 'FD'
    RESEARCH = 'RES'
    FORESTRY = 'FOR'
    ENERGY = 'ENE'
    ENGINEERING = 'ENG'
    TELECOMMUNICATIONS = 'TELE'
    INFRASTRUCTURE = 'INFRA'
    PHARMACEUTICAL = 'PHARMA'

    CATEGORY_CHOICES = [
        (MANUFACTURING, 'Manufacturing'),
        (PRODUCTION, 'Production'),
        (AGRICULTURE, 'Agriculture'),
        (CONSTRUCTION, 'Construction'),
        (RETAIL, 'Retail'),
        (MINING, 'Mining'),
        (MARKET_RESEARCH, 'Market Research'),
        (FINANCE, 'Finance'),
        (ECONOMICS, 'Economics'),
        (EDUCATION, 'Education'),
        (CHEMICALS, 'Chemicals'),
        (ADVERTISING, 'Advertising'),
        (GOODS, 'Goods'),
        (REAL_ESTATE, 'Real Estate'),
        (HEALTHCARE, 'Healthcare'),
        (FOOD, 'Food'),
        (RESEARCH, 'Research'),
        (FORESTRY, 'Forestry'),
        (ENERGY, 'Energy'),
        (INFRASTRUCTURE, 'Infrastructure'),
        (ENGINEERING, 'Engineering'),
        (TELECOMMUNICATIONS, 'Telecommunications'),
        (PHARMACEUTICAL, 'Pharmaceutical')
    ]
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True, null=True)
    company_name = models.CharField(max_length=200, null=True)
    address = models.TextField(max_length=200, null=True)
    industry = models.CharField(null=True, max_length=100)
    phone_number = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)
    user_type = models.CharField(max_length=20, null=True)
    date_joined = models.DateTimeField(verbose_name='date_joined',
                                       auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'address', 'industry', 'phone_number', 'website', 'user_type']

    objects = UserManager()

    def get_user_type_label(self):
        return UserType(self.type).name.title()

    def __str__(self):
        return self.email


class Supplier(models.Model):
    supplier = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.supplier.email


class Contractor(models.Model):
    contractor = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='contractor',
        on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.contractor.email


class Tender(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    budget = models.IntegerField(null=True)
    deadline = models.DateTimeField(null=True)
    opening_date = models.DateTimeField(verbose_name='opening_date', auto_now_add=True)
    contractor = models.ForeignKey(Contractor, related_name='tenders', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=200, null=True)
    bid_price = models.IntegerField(null=True)
    submission_date = models.DateTimeField(verbose_name='submission_date', auto_now_add=True)
    tender_id = models.ForeignKey(Tender, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='bids', on_delete=models.CASCADE)

    def __str__(self):
        return self.id
