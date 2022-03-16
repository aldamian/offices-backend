from .models import Desk
from .serializers import DeskSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Desks
class DeskList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer

    def list(self, request):
        desks = Desk.objects.all()
        serializer = DeskSerializer(desks, many=True)
        return Response(serializer.data)

    # create a new desk
    def create(self, request):
        serializer = DeskSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            desk = Desk.objects.create(
                office_id=serializer.validated_data['office_id'],
                desk_number=serializer.validated_data['desk_number'],
                user_id=serializer.validated_data['user_id'],
                is_usable=serializer.validated_data['is_usable'],
                x_size_m=serializer.validated_data['x_size_m'],
                y_size_m=serializer.validated_data['y_size_m'],
                x_pos_px=serializer.validated_data['x_pos_px'],
                y_pos_px=serializer.validated_data['y_pos_px'],
            )
            desk.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a desk
    def update(self, request, pk=None):
        desk = get_object_or_404(Desk, pk=pk)
        serializer = DeskSerializer(desk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a desk 
    # to-do: can delete only if no user is assigned
    def destroy(self, request, pk=None):
        desk = get_object_or_404(Desk, pk=pk)
        desk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)