from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('', include('hospital.urls')),
    path('manage/', admin.site.urls),
    path('ai/', include('ai_ml_system.urls')),
    path('patient/', include('patient_ms.urls')),
    path('appointment/', include('appointment.urls')),

    path('core/', include('Core.urls')),
    path('core/api/', include('API.urls')),
    path('api/', include('patient_ms.api.urls')),
]

if settings.DEBUG:
    # static
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    # debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns