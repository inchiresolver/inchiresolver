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
        return "API Root Resource"

    def get_view_description(self, html=False):
        if os.environ['INCHI_RESOLVER_TITLE'] == '':
            title = 'InChI Resolver'
        else:
            title = os.environ.get('INCHI_RESOLVER_TITLE', 'InChI Resolver')
        text = "API Root resource of the " + title + \
               ". It lists the top-level resources generally available at this and any InChI Resolver instance."
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


class ResourceModelViewSet(ModelViewSet):

    def get_view_name(self, *args, **kwargs):
        text = self.name
        if hasattr(self, 'suffix') and self.suffix:
            text += ' ' + self.suffix
        if hasattr(self, 'kwargs'):
            if 'related_field' in self.kwargs:
                text += " Instance: Related " + str(self.kwargs['related_field']).capitalize()
        return text


class ResourceRelationshipView(RelationshipView):

    def get_view_name(self, *args, **kwargs):
        text = self.name
        if hasattr(self, 'kwargs'):
            if 'related_field' in self.kwargs:
                if str(self.kwargs['related_field'])[-1] == "s":
                    field = str(self.kwargs['related_field'])[0:-1]
                else:
                    field = str(self.kwargs['related_field'])
                text += " Instance: " + field.capitalize() + " Relationship"
        return text

    def get_view_description(self, html=False):
        text = """
            This resource provides a relationship link which allows for the manipulation (creation, deletion) of this
            relationship by a client.
        """
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text


### INCHI ###

class InchiViewSet(ResourceModelViewSet):
    """
        This resource of the Resolver API provides a browsable index of all InChI structure identifiers available at
        this InChI resolver instance and its underlying service API entrypoints. Each InChI instance may provide links
        (relationships) to the service API entrypoints where it is available.
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        super().__init__(*args, **kwargs)

    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'key': ('icontains', 'iexact', 'contains'),
        'string': ('icontains', 'iexact', 'contains'),
    }
    search_fields = ('string', 'key',)


class InchiRelationshipView(ResourceRelationshipView):

    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        super().__init__(*args, **kwargs)

    queryset = Inchi.objects.all()
    self_link_view_name = 'inchi-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### ORGANZATION ###

class OrganizationViewSet(ResourceModelViewSet):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Organisation"
        super().__init__(*args, **kwargs)

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class OrganizationRelationshipView(ResourceRelationshipView):
    """
    """

    def __init__(self, *args, **kwargs):
        self.name = "Organization"
        super().__init__(*args, **kwargs)

    queryset = Organization.objects.all()
    self_link_view_name = 'organization-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### PUBLISHER ###

class PublisherViewSet(ResourceModelViewSet):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Publisher"
        super().__init__(*args, **kwargs)

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PublisherRelationshipView(ResourceRelationshipView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Publisher"
        super().__init__(*args, **kwargs)

    queryset = Publisher.objects.all()
    self_link_view_name = 'publisher-relationships'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


### ENTRYPOINT ###

class EntryPointViewSet(ResourceModelViewSet):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Entrypoint"
        super().__init__(*args, **kwargs)

    queryset = EntryPoint.objects.all()
    serializer_class = EntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EntryPointRelationshipView(ResourceRelationshipView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Entrypoint"
        super().__init__(*args, **kwargs)

    queryset = EntryPoint.objects.all()
    self_link_view_name = 'entrypoint-relationships'


### ENDPOINT ###

class EndPointViewSet(ResourceModelViewSet):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Endpoint"
        super().__init__(*args, **kwargs)

    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EndPointRelationshipView(ResourceRelationshipView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Endpoint"
        super().__init__(*args, **kwargs)

    queryset = EndPoint.objects.all()
    self_link_view_name = 'endpoint-relationships'

