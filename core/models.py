from django.db import models
from django.contrib.auth.models import User


class Contractor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    company_address = models.CharField(max_length=200, null=True)
    industry = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email_address = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Tenders(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    budget = models.IntegerField(null=True)
    opening_date = models.DateTimeField(null=False)
    deadline = models.DateTimeField(null=False)
    # contractor_id = models.ForeignKey(Contractor, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=200, null=True)
    bid_price = models.IntegerField(null=True)
    submission_date = models.DateTimeField(max_length=50, null=False)
    tender_id = models.ForeignKey(Tenders, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
