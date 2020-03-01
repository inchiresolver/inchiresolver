from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from rest_framework import permissions, routers, generics
from rest_framework.utils import formatting
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
    This appears where the docstring goes!
    """
    def get_view_name(self) -> str:
        return "Resolver API Root"

    def get_view_description(self, html=False) -> str:
        text = "Root entrypoint of the InChI Resolver"
        if html:
            return mark_safe(f"<p>{text}</p>")
        else:
            return text



# def api_root_view_name(self):
#     return "Resolver API Root"
#
#
# def api_root_view_description(self, html):
#     description_string = "Root resource of this InChI Resolver instance"
#     description = formatting.dedent(smart_str(description_string))
#     if html:
#         return formatting.markup_description(description)
#     return description


# def get_view_name(view):
#     """
#     Given a view instance, return a textual name to represent the view.
#     This name is used in the browsable API, and in OPTIONS responses.
#
#     This function is the default for the `VIEW_NAME_FUNCTION` setting.
#     """
#     # Name may be set by some Views, such as a ViewSet.
#     name = getattr(view, 'name', None)
#     if name is not None:
#         return name
#
#     name = view.__class__.__name__
#     name = formatting.remove_trailing_string(name, 'View')
#     name = formatting.remove_trailing_string(name, 'ViewSet')
#     name = formatting.camelcase_to_spaces(name)
#
#     # Suffix may be set by some Views, such as a ViewSet.
#     suffix = getattr(view, 'suffix', None)
#     if suffix:
#         name += ' ' + suffix
#
#     return name


### INCHI ###

class InchiViewSet(ModelViewSet):
    """
        The Resolver API InChI entrypoint may provide a browsable index of all InChI structure identifiers available at
        this InChI resolver instance and its underlying service API entrypoints. Each InChI may provide links
        (relationships) to the service API entrypoints where it is available.
    """
    def __init__(self, *args, **kwargs):
        self.name = "InChI"
        if 'suffix' in kwargs:
            self.name += ' ' + kwargs['suffix']
        super().__init__(*args, **kwargs)

    queryset = Inchi.objects.all()
    serializer_class = InchiSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = {
        'key': ('icontains', 'iexact', 'contains'),
        'string': ('icontains', 'iexact', 'contains'),
    }
    search_fields = ('string', 'key',)


class InchiRelationshipView(RelationshipView):
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

