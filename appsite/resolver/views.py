from rest_framework import mixins
from rest_framework import viewsets, permissions
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from resolver.models import Inchi, Organization, Publisher, UrlEntryPoint, UriEndPoint
from resolver.serializers import InchiSerializer, OrganizationSerializer, PublisherSerializer, \
    UrlEntryPointSerializer, UriEndPointSerializer


class InchiViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
    """
    """
    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('uid', 'key', 'string', 'block1', 'block2', 'block3', 'is_standard')
    
    
class OrganizationViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('uid', 'name', 'abbreviation',)
    
    
class PublisherViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('uid', 'organization', 'name', 'group', 'contact',)


class UrlEntryPointViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = UrlEntryPoint.objects.all()
    serializer_class = UrlEntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('uid', 'parent', 'publisher', 'is_inchi_resolver',)


class UriEndPointViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = UriEndPoint.objects.all()
    serializer_class = UriEndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('uid', 'entrypoint', 'media_type',)
