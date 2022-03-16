from .models import Request
from .serializers import RequestSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Requests
class RequestList(viewsets.ViewSet):
    # prod - change permission_classes to [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer

    def list(self, request):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user, token = response
            role = token.get('role')
            if role == 'Admin':
                # get remote pending requests
                requests = Request.objects.filter(status='P', remote_percentage__gt=0)
                return Response(RequestSerializer(requests, many=True).data)
            elif role == 'Office Admin':
                # get desk requests
                # requests = Request.objects.filter(status='P', )
                pass
                

            

    # create a new request
    def create(self, request):
        serializer = RequestSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            request = Request.objects.create(
                office_id=serializer.validated_data['office_id'],
                user_id=serializer.validated_data['user_id'],
                is_approved=serializer.validated_data['is_approved'],
                is_rejected=serializer.validated_data['is_rejected'],
                is_cancelled=serializer.validated_data['is_cancelled'],
            )
            request.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

