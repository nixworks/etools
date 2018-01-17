from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from mock import Mock

from EquiTrack.factories import CountryFactory, ProfileFactory
from EquiTrack.tests.mixins import FastTenantTestCase
from partners.templatetags import userprofile_tags as tags


class TestShowCountrySelect(FastTenantTestCase):
    def setUp(self):
        super(TestShowCountrySelect, self).setUp()
        self.country = CountryFactory()
        self.profile = ProfileFactory(country=self.country)
        self.profile.countries_available.add(self.country)

    def test_no_profile(self):
        self.assertEqual(tags.show_country_select({}, None), "")

    def test_country_single(self):
        res = tags.show_country_select({}, self.profile)
        self.assertEqual(
            res,
            '<select id="country_selection">'
            '<option value="{}" selected>{}</option></select>'.format(
                self.country.pk,
                self.country.name
            )
        )

    def test_country_opts(self):
        mock_opts = Mock(app_label="reports")
        res = tags.show_country_select({"opts": mock_opts}, self.profile)
        self.assertEqual(
            res,
            '<select id="country_selection">'
            '<option value="{}" selected>{}</option></select>'.format(
                self.country.pk,
                self.country.name
            )
        )
