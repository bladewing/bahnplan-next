# Create your tests here.
from django.db import IntegrityError
from django.test import TestCase

from core.models.company import Company
from core.tests.utils import login_user


class CompanyModelTest(TestCase):
    def test_check_default_no_companies(self):
        login_user(self)

        self.assertEquals(self.user.company_set.all().count(), 0)
        self.assertEquals(Company.objects.all().count(), 0)

    def test_create_company_valid_one_owner(self):
        login_user(self)
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)
        self.assertEquals(self.user.company_set.all().count(), 1)

    def test_create_company_valid_two_owners(self):
        login_user(self)
        first_user = self.user
        login_user(context=self, username='testuser2')
        second_user = self.user
        company = Company.create_owned_company(name="Testbahn", abbrev="TB", owners=[first_user, second_user])
        self.assertEquals(first_user.company_set.all().count(), 1)
        self.assertEquals(second_user.company_set.all().count(), 1)
        self.assertEquals(company.ownership.all().count(), 2)

    def test_create_company_duplicate_name(self):
        login_user(self)
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)

        with self.assertRaises(IntegrityError, msg="Adding a company with existing name should not work."):
            Company.create_owned_company(name="Testbahn", abbrev="TeB", owners=self.user)

    def test_create_company_duplicate_abbrev(self):
        login_user(self)
        Company.create_owned_company(name="Testbahn", abbrev="TB", owners=self.user)

        with self.assertRaises(IntegrityError, msg="Adding a company with existing abbreviation, should not work"):
            Company.create_owned_company(name="Tolle Bahn", abbrev="TB", owners=self.user)

    def test_create_company_to_string(self):
        login_user(self)
        company = Company.create_owned_company(name="TestBahn", abbrev="TB", owners=self.user)
        self.assertEquals(company.__str__(), "TestBahn (TB)")
