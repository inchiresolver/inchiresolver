from rest_framework.fields import MultipleChoiceField
from rest_framework_json_api import serializers
from rest_framework_json_api import relations

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint


class InchiSerializer(serializers.HyperlinkedModelSerializer):

    entrypoints = relations.ResourceRelatedField(
        queryset=EntryPoint.objects,
        many=True,
        read_only=False,
        required=False,
        related_link_view_name='inchi-related',
        related_link_url_kwarg='pk',
        self_link_view_name='inchi-relationships',
    )

    included_serializers = {
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = Inchi
        fields = ('url', 'string', 'key', 'version', 'is_standard', 'safe_options',  'entrypoints', 'added', 'modified')
        read_only_fields = ('key', 'version', 'is_standard')
        meta_fields = ('added', 'modified')

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=Organization.objects, many=False, read_only=False, required=False,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    children = relations.ResourceRelatedField(
        queryset=Organization.objects, many=True, read_only=False, required=False,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    publishers = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=True, read_only=False, required=False,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    included_serializers = {
        'parent': 'resolver.serializers.OrganizationSerializer',
        'children': 'resolver.serializers.OrganizationSerializer',
        'publishers': 'resolver.serializers.PublisherSerializer',
    }

    class Meta:
        model = Organization
        fields = ('url', 'parent', 'children', 'name', 'abbreviation', 'href', 'publishers', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=False, read_only=False, required=False,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    children = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=True, read_only=False, required=False,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    organization = relations.ResourceRelatedField(
        queryset=Organization.objects, many=False, read_only=False, required=False,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    entrypoints = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=True, read_only=False, required=False,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    included_serializers = {
        'parent': 'resolver.serializers.PublisherSerializer',
        'children': 'resolver.serializers.PublisherSerializer',
        'organization': 'resolver.serializers.OrganizationSerializer',
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = Publisher
        fields = ('url', 'parent', 'children', 'organization', 'entrypoints', 'name', 'category', 'email',
                  'address', 'href', 'orcid', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data):
        publisher = Publisher.create(**validated_data)
        publisher.save()
        return publisher


class EntryPointSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=False, read_only=False, required=False,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    children = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=True, read_only=False, required=False,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    publisher = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=False, read_only=False, required=False,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    endpoints = relations.ResourceRelatedField(
        queryset=EndPoint.objects, many=True, read_only=False, required=False,
        related_link_view_name = 'entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    included_serializers = {
        'parent': 'resolver.serializers.EntryPointSerializer',
        'children': 'resolver.serializers.EntryPointSerializer',
        'publisher': 'resolver.serializers.PublisherSerializer',
        'endpoints': 'resolver.serializers.EndPointSerializer',
    }

    class Meta:
        model = EntryPoint
        fields = ('url', 'parent', 'children', 'publisher', 'name', 'description',
                  'category', 'href', 'entrypoint_href', 'endpoints', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data):
        entrypoint = EntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class EndPointSerializer(serializers.HyperlinkedModelSerializer):

    entrypoint = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=False, read_only=False,
        related_link_view_name='endpoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='endpoint-relationships',
    )

    included_serializers = {
        'entrypoint': 'resolver.serializers.EntryPointSerializer',
    }

    request_methods = MultipleChoiceField(choices=(
        ('GET', 'GET'),
        ('POST', 'POST'),
    ), default=['GET'])

    class Meta:
        model = EndPoint
        fields = ('url', 'entrypoint', 'description', 'category', 'uri', 'request_methods', 'content_media_type', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data):
        endpoint = EndPoint.create(**validated_data)
        endpoint.save()
        return endpoint

