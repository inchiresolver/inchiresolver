from rest_framework import mixins
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend

from resolver.models import Inchi, Organization, Publisher, UrlEntryPoint, UriEndPoint
from resolver.serializers import InchiSerializer, OrganizationSerializer, PublisherSerializer, \
    UrlEntryPointSerializer, UriEndPointSerializer

from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'inchis': reverse('inchi-list', request=request, format=format),
        'organizations': reverse('organization-list', request=request, format=format),
        'publishers': reverse('publisher-list', request=request, format=format),
        'entrypoints': reverse('urlentrypoint-list', request=request, format=format),
        'endpoints': reverse('uriendpoint-list', request=request, format=format),

    })


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
