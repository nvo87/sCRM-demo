from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import views as api_views
from .api.views import UserProfileViewSet

app_name = 'accounts'

router = DefaultRouter()

router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('employee/login/', api_views.EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/register/', api_views.EmployeeRegisterView.as_view(), name='employee-register'),
]
