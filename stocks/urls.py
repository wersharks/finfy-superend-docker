from django.urls import path, include
from stocks.views import newsApi

urlpatterns = [
    path('news', newsApi.as_view()),
]