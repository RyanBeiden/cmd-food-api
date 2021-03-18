import os
import uuid
import base64
import cloudinary
from django.db import models
from rest_framework import status
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from cmdfoodapi.models import Shopper, Location


class ProfileViewSet(ModelViewSet):
    '''
    Handles profile image upload and profile edits
    '''

    # def create(self, request):
    #     shopper = Shopper.objects.get(user=request.auth.user)
    #     image_upload = ''

    #     # Format new post image & Upload to Cloudinary
    #     if request.data['profile_img']:
    #         format, imgstr = request.data['profile_img'].split(';base64,')
    #         ext = format.split('/')[-1]
    #         image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')
    #         result = cloudinary.uploader.upload(image_data, public_id=f"cmd-food-assets/media/profiles/{shopper.id}-{uuid.uuid4()}")
    #         image_upload = result['url'].split('media')[-1]

    #     shopper.profile_img = image_upload

    #     try:
    #         shopper.save()
    #         serializer = ProfileSerializer(shopper, context={'request': request})
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except ValidationError as ex:
    #         return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        shopper = Shopper.objects.get(user=request.auth.user)
        image_data = ''

        # Check for an image update
        shopper_image = shopper.profile_img.name
        image_path = request.data['profile_img'].split('media/')
        
        if image_path[-1] == shopper_image:
            image_data = image_path[1]

        # Format new profile image
        elif request.data['profile_img']:
            format, imgstr = request.data['profile_img'].split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')
            result = cloudinary.uploader.upload(image_data, public_id=f"cmd-food-assets/media/profiles/{shopper.id}-{uuid.uuid4()}")
            image_data = result['url'].split('media')[-1]

        # shopper.user = User.objects.get(id=request.auth.user)
        shopper.current_store = Location.objects.get(id=request.data['current_store'])
        shopper.profile_img = image_data

        try:
            shopper.save()
            serializer = ProfileSerializer(shopper, context={'request': request})
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    @receiver(models.signals.pre_save, sender=Shopper)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        # Deletes old file from filesystem when corresponding `Shopper` object is updated with new file.

        if not instance.pk:
            return False

        try:
            old_file = Shopper.objects.get(pk=instance.pk).profile_img
        except Shopper.DoesNotExist:
            return False

        new_file = instance.profile_img
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)



class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializer for Shopper data
    '''
    
    class Meta:
        model = Shopper
        fields = ('id', 'user', 'profile_img', 'current_store')
        depth = 1
