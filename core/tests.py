from django.test import TestCase
from core.models import *
import datetime


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

class TenderTestCase(TestCase):
    def setUp(self):
        Tender.objects.create(category="Production", notice_number="R1567-G78",
                              tender_name="Testing Tender",
                              requirement_details="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin "
                                                  "nulla nisi, finibus quis justo sed, porttitor aliquam enim. Donec "
                                                  "aliquam arcu quis dapibus suscipit. In ex ante, vehicula venenatis "
                                                  "massa iaculis, mattis consectetur nisl. Phasellus faucibus urna et "
                                                  "felis commodo finibus. Praesent mattis facilisis malesuada. "
                                                  "Vestibulum a erat tempus, viverra ante sit amet, ultricies diam. "
                                                  "Quisque vitae dolor est. Duis sem nisl, volutpat non posuere at,"
                                                  " porta id lacus. Nam eu arcu nulla. Donec sed felis vitae felis "
                                                  "mattis imperdiet. Nam feugiat egestas turpis vel ultrices. Duis "
                                                  "bibendum viverra ante, ut pharetra diam dapibus quis. Sed semper "
                                                  "quis nisl id tristique. Aliquam rhoncus, lectus a sollicitudin "
                                                  "porttitor, turpis mi condimentum urna, sit amet pretium felis "
                                                  "neque quis ligula. Maecenas id risus lacus. Phasellus ornare, "
                                                  "neque at ornare sagittis, nulla sem rhoncus leo, in efficitur ante "
                                                  "velit sed nisl. Cras ac ultricies lorem, eget consequat dolor. "
                                                  "Phasellus at metus purus. Morbi nec leo libero. Nunc rhoncus "
                                                  "hendrerit luctus. Aenean erat sapien, semper vel mi a, rhoncus "
                                                  "ullamcorper erat. Vivamus nec dapibus ipsum. Cras ac enim elit. "
                                                  "Mauris tempor erat nec diam ultricies, non pulvinar dolor tempus. "
                                                  "Integer turpis leo, gravida id pharetra viverra, blandit volutpat "
                                                  "nunc. Donec vitae justo sit amet est rhoncus viverra vitae ac arcu. "
                                                  "Nunc ultricies id nibh quis mollis. Pellentesque nibh nisl, volutpat"
                                                  " ut tellus vel, suscipit vehicula eros. Donec et dolor consectetur, "
                                                  "pharetra erat ultricies, interdum mi. Integer et vestibulum erat. "
                                                  "Mauris volutpat vulputate nisl ut molestie. Ut facilisis massa vel "
                                                  "erat hendrerit, eu accumsan nunc.",
                              budget=115000, deadline="2023-04-12 20:25:07.001830",
                              owner="testingcontractors@tests.com")

    def test_tender_creation(self):
        tender = Tender.objects.get(notice_number="R1567-G78")
