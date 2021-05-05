from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import views as api_views
from .api.views import ClubViewSet

app_name = 'clubs'

router = DefaultRouter()

router.register(r'clubs', ClubViewSet, basename='club')

urlpatterns = [
    path('', include(router.urls))
]
