from django.urls import path

from .api import views as api_views
from .api.routers import urlpatterns as router_urls

app_name = 'accounts'

urlpatterns = [
    path('employee/login/', api_views.EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/register/', api_views.EmployeeRegisterView.as_view(), name='employee-register'),
]

urlpatterns += router_urls
