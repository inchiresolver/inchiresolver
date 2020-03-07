import os

from django.utils.safestring import mark_safe
from rest_framework import permissions, routers, generics
from rest_framework_json_api.views import RelationshipView, ModelViewSet

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint
from resolver.serializers import (
    InchiSerializer,
    OrganizationSerializer,
    PublisherSerializer,
    EntryPointSerializer,
    EndPointSerializer
)


class ResolverApiView(routers.APIRootView):
    """
    Wrapper class for setting API root view name and description
    """
    def get_view_name(self):
        return "Resolver API Root"

    def get_view_description(self, html=False):
        if os.environ['INCHI_RESOLVER_TITLE'] == '':
            title = 'InChI Resolver'
        else:
            title = os.environ.get('INCHI_RESOLVER_TITLE', 'InChI Resolver')
        text = "API Root entrypoint of the " + title
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


### INCHI ###

class InchiViewSet(ModelViewSet):
    """
        The InChI entrypoint of the Resolver API may provide a browsable index of all InChI structure identifiers available at
        this InChI resolver instance and its underlying service API entrypoints. Each InChI instance may provide links
        (relationships) to the service API entrypoints where it is available.
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        if 'suffix' in kwargs:
            self.name += ' ' + kwargs['suffix']
        super().__init__(*args, **kwargs)

    def get_view_description(self, html=False, *args, **kwargs):
        text = "InchiD " + str(self.kwargs) + " x " + str(kwargs)
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text

    def get_view_name(self, *args, **kwargs):
        text = "InchiN " + str(kwargs) + "x"
        return text

    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'key': ('icontains', 'iexact', 'contains'),
        'string': ('icontains', 'iexact', 'contains'),
    }
    search_fields = ('string', 'key',)


class InchiRelatedViewSet(ModelViewSet):
    """
       List of type instances related to this InChI instance.
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI Related Type Instances"
        if 'suffix' in kwargs:
            self.name += ' ' + kwargs['suffix']
        super().__init__(*args, **kwargs)

    def get_view_description(self, html=False):
        text = "ZZZ " + str(self.kwargs) + "x"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class InchiRelationshipView(RelationshipView):
    """
        Bla
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        if 'suffix' in kwargs:
            self.name += ' ' + kwargs['suffix']
        super().__init__(*args, **kwargs)

    queryset = Inchi.objects.all()
    self_link_view_name = 'inchi-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### ORGANZATION ###

class OrganizationViewSet(ModelViewSet):
    """
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrganizationRelationshipView(RelationshipView):
    """
    """
    queryset = Organization.objects.all()
    self_link_view_name = 'organization-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### PUBLISHER ###

class PublisherViewSet(ModelViewSet):
    """
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PublisherRelationshipView(RelationshipView):
    """
    """
    queryset = Publisher.objects.all()
    self_link_view_name = 'publisher-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### ENTRYPOINT ###

class EntryPointViewSet(ModelViewSet):
    """
    """
    queryset = EntryPoint.objects.all()
    serializer_class = EntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EntryPointRelationshipView(RelationshipView):
    """
    """
    queryset = EntryPoint.objects.all()
    self_link_view_name = 'entrypoint-relationships'


### ENDPOINT ###

class EndPointViewSet(ModelViewSet):
    """
    """
    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EndPointRelationshipView(RelationshipView):
    """
    """
    queryset = EndPoint.objects.all()
    self_link_view_name = 'endpoint-relationships'

