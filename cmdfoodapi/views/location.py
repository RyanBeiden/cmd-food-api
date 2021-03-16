from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from cmdfoodapi.models import Location


class LocationViewSet(ViewSet):
    '''
    Handles creating and listing (all and individually) locations
    '''

    def retrieve(self, request, pk=None):
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        locations = Location.objects.all()

        serializer = LocationSerializer(
            locations, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):

        location = Location()
        location.name = request.data['name']
        location.city = request.data['city']
        location.state = request.data['state']
        location.zip_code = request.data['zip_code']
        location.kroger_id = request.data['kroger_id']

        try:
            location.save()
            serializer = LocationSerializer(location, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


class LocationSerializer(serializers.ModelSerializer):
    '''
    Serializer for all Location data
    '''
    
    class Meta:
        model = Location
        fields = ('id', 'url', 'name', 'city', 'state', 'zip_code', 'kroger_id')
