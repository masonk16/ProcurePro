from django.test import TestCase
from core.models import *


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="testingcontractors@tests.com", company_name="Contracting Test Company",
                            address="Contracting Address, 54 Street", industry="Telecommunications",
                            phone_number="+263711234557", website="https://www.procurepro.tech/",
                            user_type="Contractors")
        User.objects.create(email="testingsuppliers@tests.com", company_name="Supplying Test Company",
                            address="Supplying Address, 54 Street", industry="Agriculture",
                            phone_number="+263711234556", website="https://www.procurepro.tech/",
                            user_type="Suppliers")

    def test_user_creation(self):
        contractor = User.objects.get(email="testingcontractors@tests.com")
        supplier = User.objects.get(email="testingsuppliers@tests.com")
