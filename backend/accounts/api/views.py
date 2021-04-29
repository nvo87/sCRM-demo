from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView

from rest_framework import viewsets

from .serializers import EmployeeRegisterSerializer, EmployeeLoginSerializer, UserProfileSerializer
from accounts.models import Profile


class EmployeeRegisterView(RegisterView):
    serializer_class = EmployeeRegisterSerializer


class EmployeeLoginView(LoginView):
    serializer_class = EmployeeLoginSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'put']
