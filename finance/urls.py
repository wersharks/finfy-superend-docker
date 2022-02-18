from django.urls import path, include
from finance.views import getMyWalletTransactions, getMyBalance,TestTransac

urlpatterns = [
    path('balance', getMyBalance.as_view()),
    path('history', getMyWalletTransactions.as_view()),
    path('test_transac', TestTransac.as_view()),
]