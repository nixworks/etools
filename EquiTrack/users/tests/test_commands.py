from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.core.management import call_command
from django.core.management.base import CommandError

from EquiTrack.tests.cases import BaseTenantTestCase
from publics.tests.factories import PublicsCurrencyFactory
from users.models import Country


class TestAddCountry(BaseTenantTestCase):
    def test_command(self):
        # Not able to actually create a tenant, so checking
        # the raises exception that this is where the command
        # failed
        name = "test"
        PublicsCurrencyFactory(code="USD")
        with self.assertRaisesRegexp(CommandError, "Can't create tenant"):
            call_command("add_country", name)

    def test_command_exception(self):
        country = Country.objects.first()
        with self.assertRaisesRegexp(CommandError, "Currency matching query"):
            call_command("add_country", country.name)
