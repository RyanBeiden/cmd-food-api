from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from cmdfoodapi.models import ProductList, Product, Location, Shopper


class ProductListViewSet(ViewSet):
    '''
    Handles the Product Lists
    '''

    def retrieve(self, request, pk=None):
        try:
            productlist = ProductList.objects.get(pk=pk)
            serializer = ProductListSerializer(productlist, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        productlists = ProductList.objects.all()

        serializer = ProductListSerializer(
            productlists, many=True, context={'request': request})
        return Response(serializer.data)

    
    def create(self, request):
        productlist = ProductList()
        productlist.product = Product.objects.get(id=request.data['product'])
        productlist.location = Location.objects.get(id=request.data['location'])
        productlist.shopper = Shopper.objects.get(user=request.auth.user)
        productlist.completed = request.data['completed']

        try:
            productlist.save()
            serializer = ProductListSerializer(productlist, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        try:
            product = ProductList.objects.get(pk=pk)
            if product.completed == True:
                product.delete()
            else:
                pass

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductList.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, pk=None):
        # Only allow updating of the `completed` field
        productlist = ProductList.objects.get(pk=pk)
        productlist.completed = request.data['completed']
        productlist.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductList
        fields = ('id', 'url', 'product', 'location',
                'shopper', 'completed')
        depth = 1
