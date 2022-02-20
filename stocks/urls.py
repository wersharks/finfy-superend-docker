from django.urls import path, include
from stocks.views import infoAPI,MyHistoryAPI,StockBuyAPI,StockSellAPI

urlpatterns = [
    path('info', infoAPI.as_view()),
    path("history", MyHistoryAPI.as_view(), name='history'),
    path("buy", StockBuyAPI.as_view(), name='buy'),
    path("sell", StockSellAPI.as_view(), name='sell'),
]