from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import bad_request, ValidationError
from rest_framework.fields import MultipleChoiceField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers
from rest_framework_json_api import relations
from typing import Dict

from resolver import defaults
from resolver.exceptions import ResourceExistsError
from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint, MediaType


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
        fields = ('url', 'string', 'key', 'version', 'is_standard', 'safe_options', 'entrypoints', 'added', 'modified')
        read_only_fields = ('key', 'version', 'is_standard')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi

    def update(self, instance: Inchi, validated_data: Dict):
        if 'string' in validated_data or 'key' in validated_data or 'version' in validated_data or \
                'is_standard' in validated_data or 'safe_options' in validated_data:
            raise IntegrityError("fields 'string', 'key', 'version', 'is_standard' and "
                                 "'safe_options' are immutable for the inchis resource")

        entrypoints = validated_data.pop('entrypoints', None)

        instance.save()

        if entrypoints:
            instance.entrypoints.bulk_update(entrypoints, bulk=True, clear=True)
        else:
            instance.entrypoints.clear(bulk=True)

        return instance


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=Organization.objects, many=False, read_only=False, required=False, default=None,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    children = relations.ResourceRelatedField(
        queryset=Organization.objects, many=True, read_only=False, required=False, default=None,
        related_link_view_name='organization-related',
        related_link_url_kwarg='pk',
        self_link_view_name='organization-relationships',
    )

    publishers = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=True, read_only=False, required=False, default=None,
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
        fields = (
        'url', 'parent', 'children', 'name', 'abbreviation', 'category', 'href', 'publishers', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        children = validated_data.pop('children', None)
        publishers = validated_data.pop('publishers', None)

        self.is_valid(raise_exception=True)

        try:
            organization = Organization.objects.get(**validated_data)
        except Organization.DoesNotExist:
            organization = Organization.create(**validated_data)
            try:
                organization.save()
            except IntegrityError as e:
                raise ResourceExistsError("organization resource already exists", code=409)
            if children:
                organization.children.add(*children, bulk=True)
            if publishers:
                organization.publishers.add(*publishers, bulk=True)
        return organization

    def update(self, instance: Organization, validated_data: Dict):
        if 'name' in validated_data or 'parent' in validated_data:
            raise IntegrityError("fields 'name' and 'parent' are immutable for the organizations resource")

        children = validated_data.pop('children', None)
        publishers = validated_data.pop('publishers', None)

        instance.abbreviation = validated_data.get('abbreviation', instance.abbreviation)
        instance.category = validated_data.get('category', instance.category)
        instance.href = validated_data.get('href', instance.href)

        instance.save()

        if children:
            instance.children.bulk_update(children, bulk=True, clear=True)
        else:
            instance.children.clear(bulk=True)
        if publishers:
            instance.publishers.bulk_update(publishers, bulk=True, clear=True)
        else:
            instance.publishers.clear(bulk=True)

        return instance


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=False, read_only=False, required=False,
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

    children = relations.ResourceRelatedField(
        queryset=Publisher.objects, many=True, read_only=False, required=False,
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
        'organization': 'resolver.serializers.OrganizationSerializer',
        'entrypoints': 'resolver.serializers.EntryPointSerializer',
        'parent': 'resolver.serializers.PublisherSerializer',
        'children': 'resolver.serializers.PublisherSerializer',
    }

    class Meta:
        model = Publisher
        fields = ('url', 'parent', 'children', 'organization', 'entrypoints', 'name', 'category', 'email',
                  'address', 'href', 'orcid', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        children = validated_data.pop('children', None)
        entrypoints = validated_data.pop('entrypoints', None)

        self.is_valid(raise_exception=True)

        try:
            publisher = Publisher.objects.get(**validated_data)
        except Publisher.DoesNotExist:
            publisher = Publisher.create(**validated_data)
            try:
                publisher.save()
            except IntegrityError as e:
                raise ResourceExistsError("organization resource already exists", code=409)
            if children:
                publisher.children.add(*children, bulk=True)
            if entrypoints:
                publisher.entrypoints.add(*entrypoints, bulk=True)
        return publisher

    def update(self, instance: Publisher, validated_data: Dict):
        if 'organization' in validated_data or 'parent' in validated_data or 'name' in validated_data:
            raise IntegrityError("fields 'organization', 'parent', and 'name' are immutable for the publishers resource")

        children = validated_data.pop('children', None)
        entrypoints = validated_data.pop('entrypoints', None)

        instance.category = validated_data.get('category', instance.category)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.href = validated_data.get('href', instance.href)
        instance.orcid = validated_data.get('orcid', instance.orcid)

        instance.save()

        if children:
            instance.children.bulk_update(children, bulk=True, clear=True)
        else:
            instance.children.clear(bulk=True)
        if entrypoints:
            instance.entrypoints.bulk_update(entrypoints, bulk=True, clear=True)
        else:
            instance.entrypoints.clear(bulk=True)

        return instance


class EntryPointSerializer(serializers.HyperlinkedModelSerializer):

    parent = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=False, read_only=False, required=False,
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

    children = relations.ResourceRelatedField(
        queryset=EntryPoint.objects, many=True, read_only=False, required=False,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    endpoints = relations.ResourceRelatedField(
        queryset=EndPoint.objects, many=True, read_only=False, required=False,
        related_link_view_name='entrypoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='entrypoint-relationships',
    )

    included_serializers = {
        'publisher': 'resolver.serializers.PublisherSerializer',
        'endpoints': 'resolver.serializers.EndPointSerializer',
        'parent': 'resolver.serializers.EntryPointSerializer',
        'children': 'resolver.serializers.EntryPointSerializer',
    }

    class Meta:
        model = EntryPoint
        fields = ('url', 'parent', 'children', 'publisher', 'name', 'description',
                  'category', 'href', 'entrypoint_href', 'endpoints', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        children = validated_data.pop('children', None)
        publishers = validated_data.pop('publishers', None)
        endpoints = validated_data.pop('endpoints', None)

        self.is_valid(raise_exception=True)

        try:
            entrypoint = EntryPoint.objects.get(**validated_data)
        except EntryPoint.DoesNotExist:
            entrypoint = EntryPoint.create(**validated_data)
            try:
                entrypoint.save()
            except IntegrityError as e:
                raise ResourceExistsError("entrypoint resource already exists", code=409)
            if children:
                entrypoint.children.add(*children, bulk=True)
            if publishers:
                entrypoint.publishers.add(*publishers, bulk=True)
            if endpoints:
                entrypoint.endpoints.add(*endpoints, bulk=True)

        return entrypoint

    def update(self, instance: EntryPoint, validated_data: Dict):
        if 'parent' in validated_data \
                or 'publisher' in validated_data \
                or 'href' in validated_data:
            raise IntegrityError("fields 'parent', 'publisher', 'href' are immutable \
            for the entrypoints resource")

        children = validated_data.pop('children', None)
        endpoints = validated_data.pop('endpoints', None)

        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.entrypoint_href = validated_data.get('entrypoint_href', instance.entrypoint_href)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)

        instance.save()

        if children:
            instance.children.bulk_update(children, bulk=True, clear=True)
        else:
            instance.children.clear(bulk=True)
        if endpoints:
            instance.children.bulk_update(endpoints, bulk=True, clear=True)
        else:
            instance.endpoints.clear(bulk=True)

        return instance


class EndPointSerializer(serializers.HyperlinkedModelSerializer):

    accept_header_mediatypes = relations.ResourceRelatedField(
        queryset=MediaType.objects, many=True, read_only=False,
        related_link_view_name='endpoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='endpoint-relationships',
    )

    content_mediatypes = relations.ResourceRelatedField(
        queryset=MediaType.objects, many=True, read_only=False,
        related_link_view_name='endpoint-related',
        related_link_url_kwarg='pk',
        self_link_view_name='endpoint-relationships',
    )

    included_serializers = {
        'entrypoint': 'resolver.serializers.EntryPointSerializer',
        'accept_header_mediatypes': 'resolver.serializers.MediaTypeSerializer',
        'content_mediatypes': 'resolver.serializers.MediaTypeSerializer',
    }

    request_methods = MultipleChoiceField(choices=defaults.http_verbs, default=['GET'])

    class Meta:
        model = EndPoint
        fields = ('url', 'entrypoint', 'description', 'category', 'uri', 'request_methods', 'accept_header_mediatypes',
                  'content_mediatypes', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        accept_header_mediatypes = validated_data.pop('accept_header_mediatypes', None)
        content_mediatypes = validated_data.pop('content_mediatypes', None)

        self.is_valid(raise_exception=True)

        try:
            endpoint = EndPoint.objects.get(**validated_data)
        except EndPoint.DoesNotExist:
            endpoint = EndPoint.create(**validated_data)
            try:
                endpoint.save()
            except IntegrityError as e:
                raise ResourceExistsError("endpoint resource already exists", code=409)
            if accept_header_mediatypes:
                endpoint.accept_header_mediatypes.add(*accept_header_mediatypes, bulk=True)
            if content_mediatypes:
                endpoint.content_mediatypes.add(*content_mediatypes, bulk=True)
        return endpoint

    def update(self, instance: EndPoint, validated_data: Dict):
        if 'entrypoint' in validated_data or 'uri' in validated_data:
            raise IntegrityError("fields 'entrypoint', and 'uri' are immutable \
            for the endpoints resource")

        accept_header_mediatypes = validated_data.pop('accept_header_mediatypes', None)
        content_mediatypes = validated_data.pop('content_mediatypes', None)

        instance.category = validated_data.get('category', instance.category)
        instance.request_methods = validated_data.get('request_methods', instance.request_methods)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if accept_header_mediatypes:
            instance.accept_header_mediatypes.bulk_update(accept_header_mediatypes, bulk=True, clear=True)
        else:
            instance.accept_header_mediatypes.clear(bulk=True)

        if content_mediatypes:
            instance.content_mediatypes.bulk_update(content_mediatypes, bulk=True, clear=True)
        else:
            instance.content_mediatypes.clear(bulk=True)

        return instance


class MediaTypeSerializer(serializers.HyperlinkedModelSerializer):

    accepting_endpoints = relations.ResourceRelatedField(
        queryset=EndPoint.objects, many=True, read_only=False,
        related_link_view_name='mediatype-related',
        related_link_url_kwarg='pk',
        self_link_view_name='mediatype-relationships',
    )

    delivering_endpoints = relations.ResourceRelatedField(
        queryset=EndPoint.objects, many=True, read_only=False,
        related_link_view_name='mediatype-related',
        related_link_url_kwarg='pk',
        self_link_view_name='mediatype-relationships',
    )

    included_serializers = {
        'accepting_endpoints': 'resolver.serializers.EndPointSerializer',
        'delivering_endpoints': 'resolver.serializers.EndPointSerializer',
    }

    class Meta:
        model = MediaType
        fields = ('url', 'name', 'description', 'accepting_endpoints', 'delivering_endpoints', 'added', 'modified')
        read_only_fields = ('added', 'modified')
        meta_fields = ('added', 'modified')

    def create(self, validated_data: Dict):
        accepting_endpoints = validated_data.pop('accepting_endpoints', None)
        delivering_endpoints = validated_data.pop('delivering_endpoints', None)

        self.is_valid(raise_exception=True)

        try:
            mediatype = MediaType.objects.get(**validated_data)
        except MediaType.DoesNotExist:
            mediatype = MediaType.create(**validated_data)
            try:
                mediatype.save()
            except IntegrityError as e:
                raise ResourceExistsError("mediatype resource already exists", code=409)
            if accepting_endpoints:
                mediatype.accepting_endpoints.add(*accepting_endpoints, bulk=True)
            if delivering_endpoints:
                mediatype.delivering_endpoints.add(*delivering_endpoints, bulk=True)
        return mediatype


    def update(self, instance: MediaType, validated_data: Dict):
        if 'name' in validated_data:
            raise IntegrityError("field 'name', is immutable for the mediatypes resource")

        accepting_endpoints = validated_data.pop('accepting_endpoints', None)
        delivering_endpoints = validated_data.pop('delivering_endpoints', None)

        instance.description = validated_data.get('description', instance.description)

        instance.save()

        if accepting_endpoints:
            instance.accepting_endpoints.bulk_update(accepting_endpoints, bulk=True, clear=True)
        else:
            instance.accepting_endpoints.clear(bulk=True)
        if delivering_endpoints:
            instance.delivering_endpoints.bulk_update(delivering_endpoints, bulk=True, clear=True)
        else:
            instance.delivering_endpoints.clear(bulk=True)

        return instance
