from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from pycoingecko import CoinGeckoAPI


from .serializers import BuyCryptoSerializer

COINS_MARKET = "bitcoin,litecoin,ethereum"

# Create your views here.
@permission_classes([IsAuthenticated])
class MyHistoryAPI(APIView):
    def get(self, request):
        user = request.user
        cryptowallet = user.crypto
        d = cryptowallet.get_all_ledger()
        return Response(d)

@permission_classes([IsAuthenticated])
class CryptoInfoAPI(APIView):
    def get(self,request):
    
        cg = CoinGeckoAPI()
        d = cg.get_price(ids='bitcoin,litecoin,ethereum', vs_currencies='inr')
        coindata = []
        for k, v in d.items():
            coindata.append({"crypto": k, "val":v['inr']})

        data = {}
        data['code'] = 1
        data['data'] = coindata

        return Response(data)


# @permission_classes([IsAuthenticated])
# class BuyCryptoAPI(APIView):
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)

#     def post(self, request):
#         data = {}
#         serializer = BuyCryptoSerializer(data=request.data)
#         if(serializer.is_valid()):
#             o = request.user.bank.operate(serializer.data['amount'], serializer.data['crypto_symbol'])
#             return Response(o)
#         else:
#             data['code'] = -1
#             data['message'] = "error while serializing data"
#             return Response(data)