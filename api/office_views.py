from .models import Office
from .serializers import OfficeSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Offices
class OfficeList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    def list(self, request):
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)

    # create a new office
    def create(self, request):
        serializer = OfficeSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            office = Office.objects.create(
                name=serializer.validated_data['name'],
                building_id=serializer.validated_data['building_id'],
                floor_number=serializer.validated_data['floor_number'],
                total_desks=serializer.validated_data['total_desks'],
                usable_desks=serializer.validated_data['usable_desks'],
                x_size_m=serializer.validated_data['x_size_m'],
                y_size_m=serializer.validated_data['y_size_m'],
                desk_ids=serializer.validated_data['desk_ids'],
                office_admin=serializer.validated_data['office_admin'],
            )
            office.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a office
    def update(self, request, pk=None):
        office = get_object_or_404(Office, pk=pk)
        serializer = OfficeSerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an office 
    # to-do: can delete only if desks are empty
    def destroy(self, request, pk=None):
        office = get_object_or_404(Office, pk=pk)
        office.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)