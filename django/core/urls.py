from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from .settings import env


urlpatterns = i18n_patterns(
    path(f'{env.str('SECRET_URL_PREFIX')}admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path(f'{env.str('SECRET_URL_PREFIX')}rosetta/', include('rosetta.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('zarinpal/', include('zarinpal.urls')),
    path('', include('shop.urls')),
)
# -- MUST BE REMOVED -- #
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# -- MUST BE REMOVED -- #
