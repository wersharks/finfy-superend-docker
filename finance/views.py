from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from finance.models import Wallet

@permission_classes([IsAuthenticated])
class getMyWalletTransactions(APIView):
    def get(self, request):
        user = request.user
        all_trans = user.wallet.get_all_my_ledger()
        return Response(all_trans)

@permission_classes([IsAuthenticated])
class getMyBalance(APIView):
    def get(self, request):
        user = request.user
        balance = user.wallet.points
        data = {}
        data['code'] = 1
        data['data'] = balance
        return Response(data)

@permission_classes([IsAuthenticated])
class TestTransac(APIView):
    def get(self, request):
        user = request.user
        amt = self.request.query_params.get('amt')
        try:
            num = int(amt)
        except Exception as e:
            data = {}
            data['code'] = -1
            data['message'] = "send a query string ?amt=_num_ for this to work"
            return Response(data)

        w = user.wallet
        data = w.operate(num)
        return Response(data)