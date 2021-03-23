from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from cmdfoodapi.models import Product


class ProductViewSet(ViewSet):
    '''
    Handles creating, listing (all & individually), and deleting products
    '''

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        products = Product.objects.all()

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):
        product = Product()
        product.kroger_id = request.data['kroger_id']
        product.name = request.data['name']
        product.price = request.data['price']
        product.image_url = request.data['image_url']
        product.aisle = request.data['aisle']

        try:
            product.save()
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializer for all product data
    '''
    
    class Meta:
        model = Product
        fields = ('id', 'kroger_id', 'url', 'name', 'price', 'image_url', 'aisle')
