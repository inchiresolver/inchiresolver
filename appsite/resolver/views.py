from rest_framework import mixins
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import GenericViewSet

from django.shortcuts import get_object_or_404

from rest_framework.response import Response

#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_json_api.views import RelationshipView, ModelViewSet

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint
from resolver.serializers import InchiSerializer, OrganizationSerializer, PublisherSerializer, \
    EntryPointSerializer, EndPointSerializer


class InchiViewSet(ModelViewSet):
    """
    """
    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class InchiRelationshipView(RelationshipView):
    queryset = Inchi.objects
    self_link_view_name = 'inchi-relationships'


class OrganizationViewSet(ModelViewSet):
    """
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PublisherViewSet(ModelViewSet):
    """
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EntryPointViewSet(ModelViewSet):
    """
    """
    queryset = EntryPoint.objects.all()
    serializer_class = EntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EntryPointRelationshipView(RelationshipView):
    """
    """
    queryset = EntryPoint.objects
    self_link_view_name = 'entrypoint-relationships'


class EndPointViewSet(ModelViewSet):
    """
    """
    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
