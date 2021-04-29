from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView

from rest_framework import viewsets

from .serializers import EmployeeRegisterSerializer, EmployeeLoginSerializer, UserProfileSerializer
from accounts.models import Profile


class EmployeeRegisterView(RegisterView):
    """ Кастомизированная регистрация сотрудника используя dj-rest-auth """
    serializer_class = EmployeeRegisterSerializer


class EmployeeLoginView(LoginView):
    """ Кастомизированный логин сотрудника используя dj-rest-auth """
    serializer_class = EmployeeLoginSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Работа с профилем юзера (доп. информация у учетной записи) """
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()
    http_method_names = ['get', 'put']
