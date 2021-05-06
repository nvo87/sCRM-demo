from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import debug_toolbar
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", TemplateView.as_view(template_name="auth.html"), name="auth", ),
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile", ),
    path('api/v1/', include('api.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
