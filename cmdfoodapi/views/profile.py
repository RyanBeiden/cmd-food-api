import uuid
import base64
import cloudinary
from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core.files.base import ContentFile
from cmdfoodapi.models import Shopper, Location

class ProfileViewSet(ViewSet):
    '''
    Handles profile image upload, profile edits and listing a single profile
    '''

    def list(self, request):
        profiles = Shopper.objects.all()
        user_id = request.auth.user

        for profile in profiles:
            if profile.user == user_id:
                profiles = profiles.filter(id=user_id.id)

        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)


    def update(self, request, pk=None):
        shopper = Shopper.objects.get(pk=pk)
        image_url = ''

        # Check for an image update
        shopper_image = shopper.profile_img.name
        image_path = request.data['profile_img'].split('media/')
        
        if image_path[-1] == shopper_image:
            image_url = image_path[1]

        # Format new profile image
        elif request.data['profile_img']:
            format, imgstr = request.data['profile_img'].split(';base64,')
            ext = format.split('/')[-1]
            image_url = ContentFile(base64.b64decode(imgstr), name=f'.{ext}')
            result = cloudinary.uploader.upload(image_url, public_id=f"cmd-food-assets/media/profiles/{shopper.id}-{uuid.uuid4()}")
            image_url = result['url'].split('media/')[-1]


        shopper.user = User.objects.get(id=pk)
        shopper.current_store = Location.objects.get(id=request.data['current_store'])
        shopper.profile_img = image_url
        shopper.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializer for all profile data
    '''
    
    class Meta:
        model = Shopper
        fields = ('id', 'user', 'profile_img', 'current_store')