import logging

from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from app.constants import PHONE_COUNTRY_PREFIX
from app.models import PhoneRange
from app.serializers import PhoneResponseSerializer, PhoneSerializer

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = 'index.html'


class PhoneViewSet(APIView):
    serializer_class = PhoneResponseSerializer
    http_method_names = ['get']

    @swagger_auto_schema(
        query_serializer=PhoneSerializer(),
        operation_summary=_('Operator identification by number'),
    )
    @action(methods=['GET'], detail=False)
    def get(self, request, *args, **kwargs):
        serializer = PhoneSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        number = serializer.data['number']

        phone_range = PhoneRange.objects.fetch_phone_range(int(number))
        response = {}

        if phone_range is not None:
            response.update(
                {
                    'number': f'{PHONE_COUNTRY_PREFIX}{number}',
                    'operator': phone_range['operator'],
                    'region': phone_range['region'],
                },
            )

        return Response(self.serializer_class(response).data, status=status.HTTP_200_OK)
