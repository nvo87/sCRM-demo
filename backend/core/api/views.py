from dj_rest_auth.registration.views import RegisterView

from core.api.serializers import EmployeeRegisterSerializer


class EmployeeRegisterView(RegisterView):
    serializer_class = EmployeeRegisterSerializer
