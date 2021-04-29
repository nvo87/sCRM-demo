from .views import UserProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='user')

urlpatterns = router.urls
