from .models import Building, Office
from .serializers import BuildingSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Buildings
class BuildingList(viewsets.ViewSet):
    permission_classes = [UserAdminPermission, UserOfficeAdminPermission]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, request):
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    # create a new building
    def create(self, request):
        serializer = BuildingSerializer(data=request.data)
        if serializer.is_valid():
            building = Building.objects.create(
                name=serializer.validated_data['name'],
                address=serializer.validated_data['address'],
                floors_count=serializer.validated_data['floors_count'],
                img_url=serializer.validated_data['img_url'],
            )
            building.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a building
    def update(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        serializer = BuildingSerializer(building, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a building 
    # to-do: can delete only if offices are empty
    def destroy(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        # can only delete building if offices are empty
        get_offices = Office.objects.filter(building_id=building.id)
        if get_offices:
            # can't delete buildings with offices
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            building.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)