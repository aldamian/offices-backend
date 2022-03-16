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
    permission_classes = [UserAuthenticatedPermission]
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
                requests = Request.objects.filter(status='P', office_id=user.office_id)
                return Response(RequestSerializer(requests, many=True).data)
            elif role == 'Employee':
                # get user requests
                requests = Request.objects.filter(user_id=user.id)
                return Response(RequestSerializer(requests, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
                

    # create a new request
    def create(self, request):
        serializer = RequestSerializer(data=request.data)
        
        if serializer.is_valid():
            active_requests = Request.objects.filter(user_id=serializer.validated_data['user_id'], status='P')
            if active_requests.count() > 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else: 
                request = Request.objects.create(
                    office_id=serializer.validated_data['office_id'],
                    user_id=serializer.validated_data['user_id'],
                    remote_percentage=serializer.validated_data['remote_percentage'],
                    request_reason=serializer.validated_data['request_reason'],
                    status=serializer.validated_data['status'],
                    reject_reason=serializer.validated_data['reject_reason'],
                )
                request.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

