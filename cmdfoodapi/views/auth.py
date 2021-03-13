import json
from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from cmdfoodapi.models import Shopper

@csrf_exempt
def register_user(request):
    '''
    Handles the creation of a new shopper for authentication.
    '''

    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    shopper = Shopper.objects.create(
        user = new_user,
        profile_img = req_body['profile_img'],
        pref_zip = req_body['pref_zip']
    )

    shopper.save()

    token = Token.objects.create(user=new_user)

    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)