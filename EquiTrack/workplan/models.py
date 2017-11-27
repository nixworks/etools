from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

from locations.models import Location
from partners.models import PartnerOrganization
from reports.models import Result
from users.models import Section


class Workplan(models.Model):
    """
    Represents a work plan for the country programme

    Relates to :model:`reports.CountryProgramme`
    """

    STATUS = (
        ("On Track", "On Track"),
        ("Constrained", "Constrained"),
        ("No Progress", "No Progress"),
        ("Target Met", "Target Met"),
    )
    status = models.CharField(max_length=32, null=True, blank=True, choices=STATUS)
    country_programme = models.ForeignKey('reports.CountryProgramme')


class WorkplanProject(models.Model):
    """
    Represents a project for the work plan

    Relates to :model:`workplan.Workplan`
    """

    workplan = models.ForeignKey('Workplan', related_name='workplan_projects')
    # TODO: add all results that belong to this workplan project


class Label(models.Model):
    """
    Represents a label
    """

    name = models.CharField(max_length=32, unique=True)


class ResultWorkplanProperty(models.Model):
    """
    Represents a result work plan property for the work plan

    Relates to :model:`workplan.Workplan`
    Relates to :model:`reports.Result`
    Relates to :model:`users.Section`
    Relates to :model:`locations.Location`
    Relates to :model:`partners.PartnerOrganization`
    Relates to :model:`auth.User`
    Relates to :model:`workplan.Label`
    """

    workplan = models.OneToOneField(Workplan)
    result = models.ForeignKey(Result, related_name='workplan_properties')
    assumptions = models.TextField(null=True, blank=True)
    STATUS = (
        ("On Track", "On Track"),
        ("Constrained", "Constrained"),
        ("No Progress", "No Progress"),
        ("Target Met", "Target Met"),
    )
    status = models.CharField(max_length=255, null=True, blank=True, choices=STATUS)
    prioritized = models.BooleanField(default=False)
    metadata = JSONField(null=True, blank=True)
    other_partners = models.CharField(max_length=2048, null=True, blank=True)
    rr_funds = models.PositiveIntegerField(null=True, blank=True)
    or_funds = models.PositiveIntegerField(null=True, blank=True)
    ore_funds = models.PositiveIntegerField(null=True, blank=True)
    total_funds = models.PositiveIntegerField(null=True, blank=True)
    sections = models.ManyToManyField(Section, related_name="sections+")
    geotag = models.ManyToManyField(Location, related_name="geotag+")
    partners = models.ManyToManyField(PartnerOrganization, related_name="partners+")
    responsible_persons = models.ManyToManyField(User, related_name="responsible_persons+")
    labels = models.ManyToManyField(Label)

    def save(self, *args, **kwargs):
        """
        Override save to calculate field total
        """
        if not(self.rr_funds is None and
               self.or_funds is None and
               self.ore_funds is None):

            rr_f = self.rr_funds or 0
            or_f = self.or_funds or 0
            ore_f = self.ore_funds or 0
            self.total_funds = rr_f + or_f + ore_f
        super(ResultWorkplanProperty, self).save(*args, **kwargs)

    @classmethod
    def has_label(cls, label_id):
        """
        Determines if a given Label is used across ResultWorkplanProperty instances.

        Args:
            label_id: id of the given Label

        Return:
            bool: True if used, False if not
        """
        return cls.objects.filter(labels__id=label_id).exists()
