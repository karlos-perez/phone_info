import logging

from django.contrib.postgres.fields import BigIntegerRangeField
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class PhoneManager(models.Manager):
    def fetch_phone_range(self, number: int) -> dict:
        return (
            self.filter(phone_range__contains=(number, number + 1))
            .order_by('load_date')
            .values('operator', 'region', 'load_date')
            .last()
        )


class PhoneRange(models.Model):
    phone_range = BigIntegerRangeField(
        _('Phone range'),
        null=False,
        blank=False,
    )
    inn = models.PositiveBigIntegerField(
        _('INN'),
        default=0,
    )
    operator = models.CharField(
        _('Operator name'),
        max_length=255,
        db_index=True,
        default='',
    )
    region = models.TextField(
        _('Region name'),
        default='',
        blank=True,
    )
    load_date = models.DateField(
        _('Loading date'),
        null=False,
        default=now,
    )

    objects = PhoneManager()

    class Meta:
        db_table = 'phone_range'
        ordering = [
            'phone_range',
        ]
        verbose_name = _('Phone number range')
        verbose_name_plural = _('Phone number ranges')
