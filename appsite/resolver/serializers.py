from rest_framework_json_api import serializers
from rest_framework_json_api import relations
from rest_framework_json_api import renderers

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint


class InchiSerializer(serializers.ModelSerializer):

    entrypoints = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=True, read_only=False, required=False
    )

    # entrypoints = relations.HyperlinkedRelatedField(
    #     #queryset=EntryPoint.objects.all(),
    #     many=True,
    #     read_only=True,
    #     required=False,
    #     related_link_view_name='inchi-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='inchi-relationships',
    #     #source='entrypoints'
    # )

    # related_serializers = {
    #     'entrypoints': 'resolver.serializers.EntryPointSerializer',
    # }

    included_serializers = {
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = Inchi
        fields = ('url', 'string', 'key', 'version', 'is_standard', 'safeopt',  'entrypoints', 'added', 'modified')
        read_only_fields = ('key', 'version', 'is_standard', 'added', 'modified')

    # class JSONAPIMeta:
    #     included_resources = ['entrypoints']

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi


class OrganizationSerializer(serializers.ModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=Organization.objects, many=False, read_only=False, required=False
    )

    publishers = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=True, read_only=False, required=False
    )

    # parent = relations.HyperlinkedRelatedField(
    #     queryset=Organization.objects,
    #     many=False,
    #     read_only=False,
    #     required=False,
    #     related_link_view_name='organization-related',
    #     #related_link_url_kwarg='pk',
    #     self_link_view_name='organization-relationships',
    # )
    #
    # publishers = relations.HyperlinkedRelatedField(
    #     queryset=Publisher.objects,
    #     many=True,
    #     read_only=False,
    #     related_link_view_name='organization-related',
    #     #related_link_url_kwarg='pk',
    #     self_link_view_name='organization-relationships',
    # )

    included_serializers = {
        'parent': 'resolver.serializers.OrganizationSerializer',
        'publishers': 'resolver.serializers.PublisherSerializer',
    }

    class Meta:
        model = Organization
        fields = ('url', 'parent', 'name', 'abbreviation', 'href', 'publishers', 'added', 'modified')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.ModelSerializer):

    organization = relations.ResourceRelatedField(
        queryset=Organization.objects, many=False, read_only=False, required=False
    )

    entrypoints = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=True, read_only=False, required=False
    )


    # organization = relations.HyperlinkedRelatedField(
    #     queryset=Organization.objects,
    #     many=False,
    #     read_only=False,
    #     related_link_view_name='publisher-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='publisher-relationships',
    # )
    #
    # entrypoints = relations.HyperlinkedRelatedField(
    #     queryset=EntryPoint.objects,
    #     many=True,
    #     read_only=False,
    #     related_link_view_name='publisher-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='publisher-relationships',
    # )

    included_serializers = {
        'organization': 'resolver.serializers.OrganizationSerializer',
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = Publisher
        fields = ('url', 'parent', 'organization', 'entrypoints', 'name', 'group', 'contact', 'href', 'added', 'modified')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        publisher = Publisher.create(**validated_data)
        publisher.save()
        return publisher


class EntryPointSerializer(serializers.ModelSerializer):

    publisher = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=False, read_only=False, required=False
    )

    inchis = relations.ResourceRelatedField(
        queryset=Inchi.objects, many=True, read_only=False, required=False
    )

    endpoints = relations.ResourceRelatedField(
        queryset=EndPoint.objects, many=True, read_only=False, required=False
    )


    # publisher = relations.HyperlinkedRelatedField(
    #     queryset=Publisher.objects,
    #     many=False,
    #     read_only=False,
    #     related_link_view_name='entrypoint-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='entrypoint-relationships',
    # )

    # inchis = relations.HyperlinkedRelatedField(
    #     queryset=Inchi.objects,
    #     many=False,
    #     read_only=False,
    #     related_link_view_name='entrypoint-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='entrypoint-relationships',
    # )

    # endpoints = relations.HyperlinkedRelatedField(
    #     queryset=EndPoint.objects,
    #     many=True,
    #     read_only=False,
    #     related_link_view_name='entrypoint-related',
    #     related_link_url_kwarg='pk',
    #     self_link_view_name='entrypoint-relationships',
    # )

    included_serializers = {
        'publisher': 'resolver.serializers.PublisherSerializer',
        'endpoints': 'resolver.serializers.EndPointSerializer',
        'inchis': 'resolver.serializers.InchiSerializer'
    }

    class Meta:
        model = EntryPoint
        fields = ('url', 'publisher', 'name', 'description', 'category', 'href', 'inchis', 'endpoints')
        read_only_fields = ('added', 'modified')

    # class JSONAPIMeta:
    #      included_resources = ['inchis']

    def create(self, validated_data):
        entrypoint = EntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class EndPointSerializer(serializers.ModelSerializer):

    entrypoint = relations.HyperlinkedRelatedField(
        queryset=EntryPoint.objects,
        many=False,
        read_only=False,
        related_link_view_name='endpoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='endpoint-relationships',
    )

    included_serializers = {
        'entrypoint': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = EndPoint
        fields = ('url', 'entrypoint', 'description', 'category', 'uri',  'media_type')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        endpoint = EndPoint.create(**validated_data)
        endpoint.save()
        return endpoint
