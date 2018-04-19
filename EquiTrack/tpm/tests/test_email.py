from django.core import mail
from django.core.management import call_command

from EquiTrack.tests.cases import BaseTenantTestCase
from tpm.tests.factories import TPMVisitFactory


class TPMVisitEmailsTestCase(BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('update_notifications')

    def test_draft(self):
        TPMVisitFactory()
        self.assertEqual(len(mail.outbox), 0)

    def test_assign(self):
        visit = TPMVisitFactory(status='pre_assigned')

        self.assertEqual(len(mail.outbox), 0)
        visit.assign()
        self.assertEqual(
            len(mail.outbox),
            visit.tpm_partner_focal_points.filter(user__email__isnull=False).count() + 1
        )

    def test_cancel(self):
        visit = TPMVisitFactory(status='draft')

        visit.cancel('Just because')
        self.assertEqual(len(mail.outbox), 0)

    def test_reject(self):
        visit = TPMVisitFactory(status='pre_tpm_rejected')

        visit.reject('Just because')
        self.assertEqual(len(mail.outbox), visit.unicef_focal_points.filter(email__isnull=False).count())

    def test_accept(self):
        visit = TPMVisitFactory(status='pre_tpm_accepted')

        visit.accept()
        self.assertEqual(len(mail.outbox), visit.unicef_focal_points.filter(email__isnull=False).count())

    def test_send_report(self):
        visit = TPMVisitFactory(status='pre_tpm_reported')

        visit.send_report()
        self.assertEqual(len(mail.outbox), visit.unicef_focal_points.filter(email__isnull=False).count())

    def test_report_rejected(self):
        visit = TPMVisitFactory(status='pre_tpm_report_rejected')

        visit.reject_report('Just because')
        self.assertEqual(len(mail.outbox), visit.tpm_partner_focal_points.filter(user__email__isnull=False).count())

    def test_approve(self):
        visit = TPMVisitFactory(status='pre_unicef_approved')

        visit.approve(notify_focal_point=True, notify_tpm_partner=True)
        self.assertEqual(
            len(mail.outbox),

            visit.unicef_focal_points.filter(email__isnull=False).count() +
            visit.tpm_partner_focal_points.filter(user__email__isnull=False).count()
        )
