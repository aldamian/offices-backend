from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


#API endpoints
class getRoutesView(APIView):
    permission_classes = [AllowAny]

    routes = [
        {'GET': '/swagger', 'description': 'API Documentation'},
        {'GET': '/admin', 'description': 'Admin Dashboard'},
        {'GET': '/api/users'},
        {'GET': '/api/users/<int:pk>'},
        {'GET': '/api/users/<int:pk>/requests'},
        {'GET': '/api/buildings'},
        {'GET': '/api/buildings/<int:pk>'},
        {'GET': '/api/offices'},
        {'GET': '/api/offices/<int:pk>'},
        {'GET': '/api/offices/<int:pk>/requests'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/approve'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/deny'},
        {'GET': '/api/desks'},
        {'GET': '/api/desks/<int:pk>'},

        {'POST': '/api/token'},
        {'POST': '/api/token/refresh'},
        {'POST': '/api/token/blacklist'},
        {'POST': '/api/me'},
    ]

    def get(self, request):
        if request.method == 'GET':
            return Response(self.routes)


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

