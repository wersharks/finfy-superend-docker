from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import numpy as np
import pandas as pd
from pycoingecko import CoinGeckoAPI

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go

from .serializers import BuyCryptoSerializer

COINS_MARKET = "bitcoin,litecoin,ethereum"

# Create your views here.
@permission_classes([IsAuthenticated])
class MyHistoryAPI(APIView):
    def get(self, request):
        user = request.user
        # ledger = user.bank.get_all_my_ledger()
        d = {"abc":123}
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

        #declare figure
        # fig = go.Figure()

        #Candlestick
        # fig.add_trace(go.Candlestick(x=data.index,
        #                 open=data['Open'],
        #                 high=data['High'],
        #                 low=data['Low'],
        #                 close=data['Close'], name = 'market data'))

        # # Add titles
        # fig.update_layout(
        #     title='Bitcoin live share price evolution',
        #     yaxis_title='Bitcoin Price (kUS Dollars)')

        # # X-Axes
        # fig.update_xaxes(
        #     rangeslider_visible=True,
        #     rangeselector=dict(
        #         buttons=list([
        #             dict(count=15, label="15m", step="minute", stepmode="backward"),
        #             dict(count=45, label="45m", step="minute", stepmode="backward"),
        #             dict(count=1, label="HTD", step="hour", stepmode="todate"),
        #             dict(count=6, label="6h", step="hour", stepmode="backward"),
        #             dict(step="all")
        #         ])
        #     )
        # )

        #Show
        # fig.show()
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