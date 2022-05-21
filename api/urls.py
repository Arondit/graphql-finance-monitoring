from django.urls import path

from api.views import CustomAuth, log_out, registration

urlpatterns = [
    path('token-auth/', CustomAuth.as_view()),
    path('register/', registration),
    path('logout/', log_out),
]
