from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/v1/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
