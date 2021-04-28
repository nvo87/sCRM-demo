from allauth.account.utils import setup_user_email
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from accounts.models import User, EmployeeUser, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'groups', 'email', 'phone']


class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'third_name', 'phone', 'email']

    def update(self, instance, validated_data):
        instance.user.phone = validated_data.pop('phone', None)
        instance.user.email = validated_data.pop('email', None)
        instance.user.clean_fields()
        instance.user.save()
        return super().update(instance, validated_data)


class EmployeeRegisterSerializer(RegisterSerializer):
    username = None

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']
        user = EmployeeUser.objects.create_user(password=password, email=email)
        setup_user_email(request, user, [])
        return user


class EmployeeLoginSerializer(LoginSerializer):
    username = None
    email = serializers.CharField(required=True, allow_blank=False, label='Email')
