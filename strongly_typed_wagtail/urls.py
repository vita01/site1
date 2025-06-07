from django.contrib import admin
from django.urls import path, include
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls
from django.conf import settings
from django.conf.urls.static import static

from home.views import ask_bot, save_advice  # ← исправлено тут

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include('home.urls')),
    path('', include(wagtail_urls)),

    # API
    path('api/ask_bot/', ask_bot, name='ask_bot'),
    path('api/save_advice/', save_advice, name='save_advice'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
