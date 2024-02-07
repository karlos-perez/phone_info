from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from app.models import PhoneRange


@admin.register(PhoneRange)
class PhoneRangeAdmin(admin.ModelAdmin):
    list_display = ('phone_range', 'operator')
    search_fields = ('operator',)
    fieldsets = (
        (
            _('Main'),
            {
                'fields': [
                    ('phone_range',),
                    ('operator', 'inn', 'region'),
                    ('load_date',),
                ],
            },
        ),
    )
