from django.db import models
from django.contrib.auth.models import User


class Contractor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    contractor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    company_address = models.CharField(max_length=200, null=True)
    industry = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email_address = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    # supplier = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    company_address = models.CharField(max_length=200, null=True)
    industry = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email_address = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
