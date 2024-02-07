from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from app.models import Operator, PhoneRange


class PhoneTestCase(TestCase):  # noqa: WPS214
    _client = APIClient()
    _number_right = 79012700000
    _number_out_range = 79000000000
    _number_wrong_code = 76012700000
    _number_wrong_country = 19012700000
    _number_wrong_len_shorter = 7901270
    _number_wrong_len_longer = 790127000001

    @classmethod
    def setUp(cls):
        operator = Operator.objects.create(inn=7743895280, name='ООО "Т2 Мобайл"')
        PhoneRange.objects.create(
            phone_range=(9012700000, 9012800000),
            operator=operator,
            region='Рязанская обл.',
        )

    def test_fetch_phone_range_right(self):
        number_right = 9012700000
        phone_range = PhoneRange.objects.fetch_phone_range(number_right)
        result = {
            'operator__name': 'ООО "Т2 Мобайл"',
            'region': 'Рязанская обл.',
        }
        self.assertDictEqual(phone_range, result)

    def test_fetch_phone_range_out_range(self):
        number_out_range = 9000000000
        phone_range = PhoneRange.objects.fetch_phone_range(number_out_range)
        self.assertEqual(phone_range, None)

    def test_fetch_phone_range_wrong_code(self):
        number_wrong_code = 6012700000
        phone_range = PhoneRange.objects.fetch_phone_range(number_wrong_code)
        self.assertEqual(phone_range, None)

    def test_fetch_phone_range_len_shorter(self):
        number_wrong_len_shorter = 901270
        phone_range = PhoneRange.objects.fetch_phone_range(number_wrong_len_shorter)
        self.assertEqual(phone_range, None)

    def test_fetch_phone_range_len_longer(self):
        number_wrong_len_longer = 790127000001
        phone_range = PhoneRange.objects.fetch_phone_range(number_wrong_len_longer)
        self.assertEqual(phone_range, None)

    def test_get_info_not_found(self):
        response = self._client.get('api/2')
        self.assertEqual(response.status_code, 404)

    def test_get_info_number_right(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_right},
        )
        self.assertEqual(response.status_code, 200)

        result = {
            'number': '79012700000',
            'operator': 'ООО "Т2 Мобайл"',
            'region': 'Рязанская обл.',
        }
        self.assertDictEqual(response.json(), result)

    def test_get_info_number_out_range(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_out_range},
        )
        self.assertEqual(response.status_code, 200)

        result = {}
        self.assertDictEqual(response.json(), result)

    def test_get_info_number_wrong_code(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_wrong_code},
        )
        self.assertEqual(response.status_code, 400)

        result = {
            'non_field_errors': ['The number code must start with 3, 4, 8 or 9'],
        }
        self.assertDictEqual(response.json(), result)

    def test_get_info_number_wrong_country(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_wrong_country},
        )
        self.assertEqual(response.status_code, 400)

        result = {
            'non_field_errors': ['Country code must start with 7'],
        }
        self.assertDictEqual(response.json(), result)

    def test_get_info_number_wrong_len_shorter(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_wrong_len_shorter},
        )
        self.assertEqual(response.status_code, 400)

        result = {
            'number': ['Убедитесь, что это значение содержит не менее 11 символов.'],
        }
        self.assertDictEqual(response.json(), result)

    def test_get_info_number_number_wrong_len_longer(self):
        response = self._client.get(
            reverse('phone-info'),
            {'number': self._number_wrong_len_longer},
        )
        self.assertEqual(response.status_code, 400)

        result = {
            'number': ['Убедитесь, что это значение содержит не более 11 символов.'],
        }
        self.assertDictEqual(response.json(), result)
