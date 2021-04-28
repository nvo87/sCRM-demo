from allauth.account.views import confirm_email as allauth_confirm_email
from dj_rest_auth.views import PasswordResetConfirmView

from django.urls import path, include
from django.http import HttpResponse


def empty_view(request):
    """ Заглушка пустого view, для того чтобы отрабатывали некоторые роуты не требующие рендеринга. """
    return HttpResponse('')


urlpatterns = [
    path('', include('accounts.urls')),
    path('api/v1/', include('dj_rest_auth.urls')),
    # данный УРЛ используется для генерации письма со ссылкой на подтверждение и для верификации email по ключу <key>.
    # настройками в settings.py верификацию можно сделать по GET или POST запросу, и добавить редирект в случае успеха.
    path('api/v1/verify-email/<key>', allauth_confirm_email, name="account_confirm_email", ),
    # вьюха, которая будет показана после успешной отправки письма для верификации
    path("confirm-email/", empty_view, name="account_email_verification_sent"),
    # работает по аналогии с account_confirm_email. В POST запросе надо выслать uid, token, password1, password2
    path('api/v1/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
