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

from bank.serializers import DepositSerializer, IDSerializer

User = get_user_model()

@permission_classes([IsAuthenticated])
class DepositBankAPI(APIView):
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
    def post(self, request):
        data = {}
        serializer = IDSerializer(data=request.data)
        if(serializer.is_valid()):
            o = request.user.bank.withdraw(serializer.data['id'])
            return Response(o)
        else:
            data['code'] = -1
            data['message'] = "error while serializing data"
            return Response(data)

@permission_classes([IsAuthenticated])
class MyHistoryAPI(APIView):
    def get(self, request):
        user = request.user
        ledger = user.bank.get_all_my_ledger()
        return Response(ledger)

def filter_open(l):
    print(l)
    if("Fixed" in l['invesType'] or not "ontenure" in l['inveStat']):
        return False
    else:
        return True

@permission_classes([IsAuthenticated])
class MyHistoryOngoingAPI(APIView):
    def get(self, request):
        user = request.user
        ledger = user.bank.get_all_my_ledger()
        data = ledger['data']
        filtered = filter(filter_open, data)
        ledger['data'] = filtered
        return Response(ledger)