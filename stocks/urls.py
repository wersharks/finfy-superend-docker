from django.urls import path, include
from stocks.views import newsApi, getStockHistory

urlpatterns = [
    path('news', newsApi.as_view()),
    path('history', getStockHistory.as_view()),
]