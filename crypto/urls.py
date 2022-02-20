from django.urls import path

# from .views import UserRegistrationView, LogoutView, UserLoginView
from .views import MyHistoryAPI, CryptoInfoAPI

urlpatterns = [
    path("info", CryptoInfoAPI.as_view(), name='info'),
    path("history", MyHistoryAPI.as_view(), name='history')
]