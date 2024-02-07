from django.urls import path

from app.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
]
