from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.constants import PHONE_CODE_PREFIX, PHONE_COUNTRY_PREFIX, PHONE_NUMBER_LENGTH


class PhoneSerializer(serializers.Serializer):
    number = serializers.CharField(
        min_length=PHONE_NUMBER_LENGTH,
        max_length=PHONE_NUMBER_LENGTH,
        help_text=_('Phone number'),
    )

    def validate(self, attrs) -> dict[str, str]:
        number: str = attrs['number']

        if not number.startswith(PHONE_COUNTRY_PREFIX):
            raise ValidationError(
                _(f'Country code must start with {PHONE_COUNTRY_PREFIX}'),
            )

        if number[1] not in PHONE_CODE_PREFIX:
            raise ValidationError(_('The number code must start with 3, 4, 8 or 9'))

        return {'number': number[1:]}


class PhoneResponseSerializer(serializers.Serializer):
    number = serializers.CharField(read_only=True)
    operator = serializers.CharField(read_only=True)
    region = serializers.CharField(read_only=True)
