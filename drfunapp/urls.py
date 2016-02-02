from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from drfundata.views import WebResourceTypeViewSet, WebResourceViewSet
from drfundata.views import WebResourceTypeHLMViewSet, WebResourceHLMViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'webresourcetypes', WebResourceTypeViewSet, base_name='webresourcetypes')
router.register(r'webresources', WebResourceViewSet, base_name='webresources')
router.register(r'webresourcetypes_linked', WebResourceTypeHLMViewSet)
router.register(r'webresources_linked', WebResourceHLMViewSet)

urlpatterns = [
    url(r'^admin/', include('smuggler.urls')),  # before admin url patterns!
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/echo/', include('echo.urls')),
    url(r'^api/v1/httpbin/', include('httpbin.urls')),
    url(r'^api/v1/transitionsfbv/', include('transitionsfbv.urls')),
    url(r'^api/v1/transitionscbv/', include('transitionscbv.urls')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    url(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
