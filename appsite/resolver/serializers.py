from rest_framework_json_api import serializers
from rest_framework_json_api import relations

from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint


class InchiSerializer(serializers.HyperlinkedModelSerializer):

    entrypoints = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=True,
        read_only=True,
        required=False,
        related_link_view_name='inchi-related',
        related_link_url_kwarg='pk',
        self_link_view_name='inchi-relationships',
    )

    related_serializers = {
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = Inchi
        fields = ('url', 'string', 'key', 'version', 'is_standard', 'safeopt', 'entrypoints', 'added', 'modified')
        read_only_fields = ('key', 'version', 'is_standard', 'added', 'modified')

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi


class OrganizationSerializer(serializers.ModelSerializer):

    parent = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=False,
        read_only=True,
        required=False,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    related_serializers = {
        'parent': 'resolver.serializers.OrganizationSerializer',
    }



    class Meta:
        model = Organization
        fields = ('url', 'parent', 'name', 'abbreviation', 'href', 'added', 'modified')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.ModelSerializer):

    organization = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=False,
        read_only=True,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    entrypoints = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=True,
        read_only=True,
        related_link_view_name='publisher-related',
        related_link_url_kwarg='pk',
        self_link_view_name='publisher-relationships',
    )

    related_serializers = {
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

    publisher = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=False,
        read_only=True,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    endpoints = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=True,
        read_only=True,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    related_serializers = {
        'publisher': 'resolver.serializers.PublisherSerializer',
        'endpoints': 'resolver.serializers.EndPointSerializer'
    }

    class Meta:
        model = EntryPoint
        fields = ('url', 'publisher', 'name', 'description', 'category', 'href', 'endpoints')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        entrypoint = EntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class EndPointSerializer(serializers.ModelSerializer):

    entrypoint = relations.HyperlinkedRelatedField(
        # queryset=EntryPoint.objects,
        many=False,
        read_only=True,
        related_link_view_name='endpoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='endpoint-relationships',
    )

    related_serializers = {
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
