from django.shortcuts import render

@permission_classes([IsAuthenticated])
class newsApi(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
