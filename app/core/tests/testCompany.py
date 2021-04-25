from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from core.models import Company


class CompanyModelTest(TestCase):
    def test_check_default_no_companies(self):
        self.login_user()

        self.assertEquals(self.user.company_set.all().count(), 0)
        self.assertEquals(Company.objects.all().count(), 0)

    def login_user(self, username='testuser', password='12345'):
        if not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_user(username=username, password=password)
        self.user = get_user_model().objects.filter(username=username).first()
        self.client.login(username=username, password=password)

    def test_create_company_valid_one_owner(self):
        self.login_user()
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)
        self.assertEquals(self.user.company_set.all().count(), 1)

    def test_create_company_valid_two_owners(self):
        self.login_user()
        first_user = self.user
        self.login_user(username='testuser2')
        second_user = self.user
        company = Company.create_owned_company(name="Testbahn", abbrev="TB", owners=[first_user, second_user])
        self.assertEquals(first_user.company_set.all().count(), 1)
        self.assertEquals(second_user.company_set.all().count(), 1)
        self.assertEquals(company.ownership.all().count(), 2)

    def test_create_company_duplicate_name(self):
        self.login_user()
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)

        with self.assertRaises(IntegrityError, msg="Adding a company with existing name should not work."):
            Company.create_owned_company(name="Testbahn", abbrev="TeB", owners=self.user)

    def test_create_company_duplicate_abbrev(self):
        self.login_user()
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)

        with self.assertRaises(IntegrityError, msg="Adding a company with existing abbreviation, should not work"):
            Company.create_owned_company(name="Tolle Bahn", abbrev="TB", owners=self.user)

    def test_create_company_string_length(self):
        self.login_user()
        Company.create_owned_company(name="", abbrev="TB", owners=self.user)
