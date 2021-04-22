from allauth.account.utils import setup_user_email
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from core.models import User, EmployeeUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'groups', 'email', 'phone']


class EmployeeRegisterSerializer(RegisterSerializer):
    username = None

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']
        user = EmployeeUser.objects.create_user(password=password, email=email)
        setup_user_email(request, user, [])
        return user
