import json
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers


@api_view(['POST'])
def registration(request):
    body = request.body.decode('utf-8')
    body = json.loads(body)
    print(body)
    username = body['username']
    email = body['email']
    already_registered = User.objects.filter(Q(username=username) | Q(email=email)).exists()

    if already_registered:
        raise ValueError('Already registered')
    
    user = User.objects.create(username=username, email=email, password=body['password'])

    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key})


class CustomAuthSerializer(AuthTokenSerializer):
    username = serializers.CharField(label=_("Username"), write_only=True, required=False)
    email = serializers.CharField(label=_("email"), style={'input_type': 'password'}, required=False)
    
    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if not email and not username or not password:
            msg = _('Missed arguments')
            raise serializers.ValidationError(msg, code='authorization')

        try:
            user = User.objects.get(Q(email=email) | Q(username=username), password=password)
        except User.DoesNotExist:
            print(User.objects.all().values('id', 'password', 'username', 'email'))
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomAuth(ObtainAuthToken):
    serializer_class = CustomAuthSerializer


@api_view(['POST'])
def log_out(request):
    logout(request)


@api_view(['POST'])
def check_auth(request):
    print(request.user)
    user = request.user
    return Response({'username': user.username, 'email': user.email})
