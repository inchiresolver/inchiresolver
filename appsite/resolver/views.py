import os

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework import permissions, routers, generics
from rest_framework.decorators import action
from rest_framework_json_api.views import RelationshipView, ModelViewSet

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint, MediaType
from resolver.serializers import (
    InchiSerializer,
    OrganizationSerializer,
    PublisherSerializer,
    EntryPointSerializer,
    EndPointSerializer,
    MediaTypeSerializer
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
        text = "**API Root** resource of the " + title.strip('"') + \
               ". It lists the top-level resources generally available at this and any InChI Resolver instance."
        if html:
            return mark_safe(f"<p>{text} For documentation <a href=\"https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst\">please see here</a>.</p>")
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
        The **InChI resource** of the InChI Resolver API. For documentation [see here][ref]
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#inchi-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        super().__init__(*args, **kwargs)

    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'id': ('exact', 'in'),
        'key': ('icontains', 'iexact', 'contains', 'exact'),
        'string': ('icontains', 'iexact', 'contains', 'exact'),
        'version': ('exact', 'in', 'gt', 'gte', 'lt', 'lte',),
        'safe_options': ('icontains', 'iexact', 'contains', 'exact'),
        'entrypoints__category': ('exact', 'in'),
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
        The **organization resource** of the InChI Resolver API. For documentation [please see here][ref].
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#organization-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "Organization"
        super().__init__(*args, **kwargs)

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'id': ('exact', 'in'),
        'name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'abbreviation': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'category': ('exact', 'in'),
        'href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent': ('exact', 'in'),
        'parent__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__abbreviation': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children': ('exact', 'in'),
        'children__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__abbreviation': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publishers__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publishers__category': ('icontains', 'iexact', 'contains', 'exact', 'in'),
    }
    search_fields = ('name', 'abbreviation', 'category', 'href')


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
        The **publisher resource** of the InChI Resolver API. For documentation [please see here][ref].
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#publisher-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "Publisher"
        super().__init__(*args, **kwargs)

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'id': ('exact', 'in'),
        'name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'category': ('exact', 'in'),
        'email': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'address': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'orcid': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__category': ('exact', 'in'),
        'parent__email': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__address': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'parent__orcid': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__category': ('exact', 'in'),
        'children__email': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__address': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'children__orcid': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'organization__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'organization__abbreviation': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'organization__category': ('icontains', 'iexact', 'contains', 'exact', 'in'),
    }
    search_fields = ('name', 'category', 'email', 'address', 'href', 'orcid')


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
        The **entrypoint resource** of the InChI Resolver API. For documentation [please see here][ref].
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#entrypoint-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "Entrypoint"
        super().__init__(*args, **kwargs)

    queryset = EntryPoint.objects.all()
    serializer_class = EntryPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False)
    def get_self_entrypoint(self, request, pk=None):
        queryset = EntryPoint.objects.filter(category='self').get()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)

    filterset_fields = {
        'id': ('exact', 'in'),
        'category': ('exact', 'in'),
        'href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publisher__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publisher__category': ('exact', 'in'),
        'publisher__email': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publisher__address': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publisher__href': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'publisher__orcid': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'endpoints__description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'endpoints__category': ('exact', 'in'),
        'endpoints__uri': ('icontains', 'iexact', 'contains', 'exact', 'in'),
    }
    search_fields = ('category', 'href', 'name', 'description')


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
        The **endpoint resource** of the InChI Resolver API. For documentation [please see here][ref].
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#endpoint-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "Endpoint"
        super().__init__(*args, **kwargs)

    queryset = EndPoint.objects.all()
    serializer_class = EndPointSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'id': ('exact', 'in'),
        'description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'category': ('exact', 'in'),
        'uri': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'entrypoint__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'entrypoint__category': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'accept_header_media_types__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'content_media_types__name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'request_schema_endpoint__description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'request_schema_endpoint__category': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'request_schema_endpoint__uri': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'response_schema_endpoint__description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'response_schema_endpoint__category': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'response_schema_endpoint__uri': ('icontains', 'iexact', 'contains', 'exact', 'in'),
    }
    search_fields = ('category', 'uri', 'description',)


class EndPointRelationshipView(ResourceRelationshipView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Endpoint"
        super().__init__(*args, **kwargs)

    queryset = EndPoint.objects.all()
    self_link_view_name = 'endpoint-relationships'


### MEDIA  TYPE ###

class MediaTypeViewSet(ResourceModelViewSet):
    """
        The **mediatype resource** of the InChI Resolver API. For documentation [please see here][ref].
        [ref]: https://github.com/inchiresolver/inchiresolver/blob/master/docs/protocol.rst#mediatype-resource
    """
    def __init__(self, *args, **kwargs):
        self.name = "Mediatype"
        super().__init__(*args, **kwargs)

    queryset = MediaType.objects.all()
    serializer_class = MediaTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'id': ('exact', 'in'),
        'name': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'description': ('icontains', 'iexact', 'contains', 'exact', 'in'),
        'accepting_endpoints': ('exact', 'in'),
        'delivering_endpoints': ('exact', 'in'),
    }
    search_fields = ('name', 'description',)


class MediaTypeRelationshipView(ResourceRelationshipView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.name = "Mediatype"
        super().__init__(*args, **kwargs)

    queryset = MediaType.objects.all()
    self_link_view_name = 'mediatype-relationships'

