from rest_framework.response import Response
from django.contrib.auth.models import User


class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response

class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.headers)
        response: Response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"

        print(response.headers)

        return response


class DummyTokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            print(request.headers)
            if 'authorization' in request.headers:
                token_header = request.headers['authorization']
            if 'Authorization' in request.headers:
                token_header = request.headers['Authorization']
            print(token_header)
            token = token_header.split(' ')[-1]
            print(token)
            user = User.objects.filter(auth_token__key=token).first()
            if not user:
                print('wtf')
            print(user)
            setattr(request, 'user', user)
            return self.get_response(request)
        except Exception as e:
            print('something get wrongf', e)
        return self.get_response(request)
