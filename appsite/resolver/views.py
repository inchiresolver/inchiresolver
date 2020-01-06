from rest_framework import mixins
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import GenericViewSet

#from django_filters.rest_framework import DjangoFilterBackend

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint
from resolver.serializers import InchiSerializer, OrganizationSerializer, PublisherSerializer, \
    EntryPointSerializer, EndPointSerializer


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
    #filter_fields = ('key', 'string', 'block1', 'block2', 'block3', 'is_standard')

    resource_name = 'inchis'
    serializer_class = InchiSerializer
    #allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    #permission_classes = (permissions.IsAuthenticated,)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #filter_fields = ('name', 'abbreviation',)
    
    
class PublisherViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #filter_fields = ('organization', 'name', 'group', 'contact',)


class EntryPointViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = EntryPoint.objects.all()
    serializer_class = EntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #filter_fields = ('parent', 'publisher', 'is_inchi_resolver',)


class EndPointViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #filter_fields = ('entrypoint', 'media_type',)
