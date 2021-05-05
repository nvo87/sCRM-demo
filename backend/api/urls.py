from allauth.account.views import confirm_email as allauth_confirm_email
from dj_rest_auth.views import PasswordResetConfirmView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from accounts.urls import router as accounts_router
from clubs.urls import router as clubs_router


def empty_view(request):
    """ Заглушка пустого view, для того чтобы отрабатывали некоторые роуты не требующие рендеринга. """
    return HttpResponse('')


schema_view = get_schema_view(
    openapi.Info(
        title='sCRM API',
        description='API для подключения клиента',
        default_version='1',
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

router = DefaultRouter()
router.registry.extend(accounts_router.registry)
router.registry.extend(clubs_router.registry)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('accounts.urls')),
    path('', include('clubs.urls')),

    path('', include('dj_rest_auth.urls')),
    # данный УРЛ используется для генерации письма со ссылкой на подтверждение и для верификации email по ключу <key>.
    # настройками в settings.py верификацию можно сделать по GET или POST запросу, и добавить редирект в случае успеха.
    path('verify-email/<key>', allauth_confirm_email, name="account_confirm_email", ),
    # вьюха, которая будет показана после успешной отправки письма для верификации
    path("confirm-email/", empty_view, name="account_email_verification_sent"),
    # работает по аналогии с account_confirm_email. В POST запросе надо выслать uid, token, password1, password2
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
