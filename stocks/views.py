from django.shortcuts import render
from django.contrib.auth import get_user_model, login, logout

import yfinance as yf
import pandas as pd
import numpy as np

from .serializers import StockActionSerializer
from .const import STOCK_MARKET

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

@permission_classes([IsAuthenticated])
class MyHistoryAPI(APIView):
    def get(self, request):
        user = request.user
        stockwallet = user.stocks
        d = stockwallet.get_all_ledger()
        return Response(d)

@permission_classes([IsAuthenticated])
class infoAPI(APIView):
    def get(self, request):
        data = []
        for stock in STOCK_MARKET:
            company_info = yf.Ticker(stock)
            hist = company_info.history(period="max")
            a = hist.to_numpy() 
            shape = a.shape
            end = shape[0]
            latest = a[end-1][3]
            one_day_prev = a[end-2][3]
            diff = latest - one_day_prev
            percentage_diff = (diff/one_day_prev)*100
            logo = company_info.info['logo_url']
            market_cap = company_info.info['marketCap']
            dividend = company_info.info['dividendYield']
            # PEratio = company_info.info['trailingPE']
            sector = company_info.info['sector']
            employees = company_info.info['fullTimeEmployees']
            summary = company_info.info['longBusinessSummary']
            news = company_info.news
            content = {'latest' : latest, 'on_day_prev' : one_day_prev, 'diff' : diff, 'percentage_diff':percentage_diff,'logo':logo,'market_cap':market_cap,'dividend':dividend,'sector':sector,'empolyees':employees,'summary':summary,'news':news}
            data.append(content)
        return Response(data)
    
@permission_classes([IsAuthenticated])
class StockBuyAPI(APIView):
    def post(self,request):
        data = {}
        serializer = StockActionSerializer(data=request.data)

        if(serializer.is_valid()):
            o = request.user.stocks.buy(serializer.data['stock_symbol'], serializer.data['amount'])
            return Response(o)
        else:
            data['code'] = -1
            data['message'] = "error while serializing data"
            return Response(data)
    
@permission_classes([IsAuthenticated])
class StockSellAPI(APIView):
    def post(self,request):
        data = {}
        serializer = StockActionSerializer(data=request.data)

        if(serializer.is_valid()):
            o = request.user.stocks.sell(serializer.data['stock_symbol'], serializer.data['amount'])
            return Response(o)
        else:
            data['code'] = -1
            data['message'] = "error while serializing data"
            return Response(data)

