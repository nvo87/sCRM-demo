from django.urls import path, include

from .api import views as api_views

app_name = 'core'

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('employee/registration/', api_views.EmployeeRegisterView.as_view()),
]
