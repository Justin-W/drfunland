from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from .models import WebResourceType, WebResource
from .serializers import WebResourceTypeSerializer, WebResourceSerializer
from .serializers import WebResourceTypeHLMSerializer, WebResourceHLMSerializer


class GenericCRUDLViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    Generic base class for all CRUDL operations
    """
    pass


class WebResourceTypeViewSet(GenericCRUDLViewSet):
    """
    ViewSet for WebResourceType
    """
    queryset = WebResourceType.objects.all()
    serializer_class = WebResourceTypeSerializer
    # serializer_class = WebResourceTypeHLMSerializer
    permission_classes = (AllowAny,)


class WebResourceViewSet(GenericCRUDLViewSet):
    """
    ViewSet CRUDL for WebResource
    """
    queryset = WebResource.objects.all()
    serializer_class = WebResourceSerializer
    # serializer_class = WebResourceHLMSerializer
    permission_classes = (AllowAny,)


class WebResourceTypeHLMViewSet(GenericCRUDLViewSet):
    """
    Hyperlinked ViewSet for WebResourceType
    """
    queryset = WebResourceType.objects.all()
    # serializer_class = WebResourceTypeSerializer
    serializer_class = WebResourceTypeHLMSerializer
    permission_classes = (AllowAny,)


class WebResourceHLMViewSet(GenericCRUDLViewSet):
    """
    Hyperlinked ViewSet for WebResource
    """
    queryset = WebResource.objects.all()
    # serializer_class = WebResourceSerializer
    serializer_class = WebResourceHLMSerializer
    permission_classes = (AllowAny,)
