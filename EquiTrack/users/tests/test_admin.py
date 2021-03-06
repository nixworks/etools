from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from mock import Mock
from unittest import skip

from EquiTrack.tests.cases import BaseTenantTestCase
from users.admin import (
    CountryAdmin,
    ProfileAdmin,
    ProfileInline,
    UserAdminPlus,
)
from users.models import Country, User, UserProfile
from users.tests.factories import ProfileFactory, UserFactory


class MockRequest:
    pass


class TestProfileInline(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        site = AdminSite()
        cls.admin = ProfileInline(UserProfile, site)
        cls.request = MockRequest()
        cls.user = UserFactory()

    def test_get_fields(self):
        """If not superuser then remove country_override"""
        self.request.user = self.user
        self.assertFalse(self.request.user.is_superuser)
        fields = self.admin.get_fields(self.request)
        self.assertNotIn("country_override", fields)

    @skip("Appears that fields are maybe cached?")
    def test_get_fields_superuser(self):
        """If superuser then country_override stays"""
        self.request.user = self.superuser
        self.assertTrue(self.request.user.is_superuser)
        fields = self.admin.get_fields(self.request)
        self.assertIn("country_override", fields)


class TestProfileAdmin(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        site = AdminSite()
        cls.admin = ProfileAdmin(UserProfile, site)
        cls.request = MockRequest()
        cls.superuser = UserFactory(is_superuser=True)
        cls.user = UserFactory()

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request))

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request))

    def test_get_fields(self):
        """If not superuser then remove country_override"""
        self.request.user = self.user
        fields = self.admin.get_fields(self.request)
        self.assertNotIn("country_override", fields)

    @skip("Appears fields is maybe cached?")
    def test_get_fields_superuser(self):
        """If superuser then country_override stays"""
        self.request.user = self.superuser
        self.assertTrue(self.request.user.is_superuser)
        fields = self.admin.get_fields(self.request)
        self.assertIn("country_override", fields)

    def test_save_model_supervisor(self):
        """If supervisor provided, then set supervisor"""
        mock_form = Mock()
        mock_form.data = {"supervisor": self.superuser.pk}
        obj = ProfileFactory()
        self.assertIsNone(obj.supervisor)
        self.admin.save_model(
            self.request,
            obj,
            mock_form,
            None)
        profile_updated = UserProfile.objects.get(pk=obj.pk)
        self.assertEqual(profile_updated.supervisor, self.superuser)

    def test_save_model_oic(self):
        """If OIC provided, then set OIC"""
        mock_form = Mock()
        mock_form.data = {"oic": self.superuser.pk}
        obj = ProfileFactory()
        self.assertIsNone(obj.oic)
        self.admin.save_model(
            self.request,
            obj,
            mock_form,
            None)
        profile_updated = UserProfile.objects.get(pk=obj.pk)
        self.assertEqual(profile_updated.oic, self.superuser)


class TestUserAdminPlus(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        site = AdminSite()
        cls.admin = UserAdminPlus(User, site)
        cls.request = MockRequest()
        cls.superuser = UserFactory(is_superuser=True)
        cls.user = UserFactory()

    def test_office(self):
        self.assertEqual(
            self.admin.office(self.user),
            self.user.profile.office
        )

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request))

    def test_has_delete_permission(self):
        self.assertFalse(self.admin.has_delete_permission(self.request))

    def test_get_readonly_fields(self):
        """If user NOT superuser then is_superuser is readonly"""
        self.request.user = self.user
        readonly_fields = self.admin.get_readonly_fields(self.request)
        self.assertIn("is_superuser", readonly_fields)

    def test_get_readonly_fields_superuser(self):
        """If user is superuser then is_superuser is NOT readonly"""
        self.request.user = self.superuser
        self.assertTrue(self.request.user.is_superuser)
        readonly_fields = self.admin.get_readonly_fields(self.request)
        self.assertNotIn("is_superuser", readonly_fields)


class TestCountryAdmin(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        site = AdminSite()
        cls.admin = CountryAdmin(Country, site)
        cls.request = MockRequest()

    def test_has_add_permission(self):
        self.assertFalse(self.admin.has_add_permission(self.request))
