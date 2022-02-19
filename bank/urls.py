from django.urls import path

# from .views import UserRegistrationView, LogoutView, UserLoginView
from bank.views import DepositBankAPI, WithdrawBankAPI, MyHistoryAPI, MyHistoryOngoingAPI

urlpatterns = [
    path("deposit", DepositBankAPI.as_view(), name='deposit'),
    path("withdraw", WithdrawBankAPI.as_view(), name='withdraw'),
    path("history", MyHistoryAPI.as_view(), name='history'),
    path("ongoingDeposits", MyHistoryOngoingAPI.as_view(), name='ongoing')
]