import contextlib
from rest_framework.response import Response


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
        with contextlib.suppress(Exception):
            if 'authorization' in request.headers:
                token_header = request.headers['authorization']
            if 'Authorization' in request.headers:
                token_header = request.headers['Authorization']
            token = token_header.split(' ')[-1]
            user = User.objects.filter(token__auth=token)
            setattr(request, 'user', user)
            return response

