from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@permission_classes([IsAuthenticated])
class newsApi(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


@permission_classes([IsAuthenticated])
class getStockHistory(APIView):
    def get(self, request):
        user = request.user
        stockwallet = user.stocks
        data = stockwallet.get_all_ledger()
        return Response(data)
