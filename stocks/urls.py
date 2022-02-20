from django.urls import path, include
from stocks.views import infoAPI

urlpatterns = [
    path('info', infoAPI.as_view()),
]