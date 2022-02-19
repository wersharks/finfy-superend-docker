from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .forms import UserRegistrationForm, UserAddressForm
from bank.serializers import DepositSerializer

User = get_user_model()

@permission_classes([IsAuthenticated])
class DepositBankAPI(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):
        data = {}
        serializer = DepositSerializer(data=request.data)
        if(serializer.is_valid()):
            o = request.user.bank.operate(serializer.data['amount'], serializer.data['inves_type'])
            return Response(o)
        else:
            data['code'] = -1
            data['message'] = "error while serializing data"
            return Response(data)


@permission_classes([IsAuthenticated])
class WithdrawBankAPI(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

@permission_classes([IsAuthenticated])
class MyHistoryAPI(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)