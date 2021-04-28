from .views import UserProfileViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserProfileViewset, basename='user')

urlpatterns = router.urls
