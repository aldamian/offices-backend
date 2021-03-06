from .models import Building, Office
from .serializers import BuildingSerializer, BuildingGetSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Display Buildings
class BuildingList(viewsets.ViewSet):
    permission_classes = [UserAdminPermission|UserOfficeAdminPermission]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, request):
        buildings = Building.objects.all()
        serializer = BuildingGetSerializer(buildings, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        serializer = BuildingSerializer(building)
        return Response(serializer.data)

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
            # building added succesfully
            return Response({"Success": "Building added succesfully."}, status=status.HTTP_201_CREATED)
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
        building.delete()
        return Response({"Success": "Building deleted succesfully."}, status=status.HTTP_204_NO_CONTENT)