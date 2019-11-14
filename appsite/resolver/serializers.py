from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse


from resolver.models import Inchi, Organization, Publisher, UrlEntryPoint, UriEndPoint


# class InchiKeySerializer(serializers.HyperlinkedModelSerializer):
#
#     self = serializers.HyperlinkedIdentityField(view_name='inchi-detail', format='html')
#
#     class Meta:
#         model = Inchi
#         fields = ('self', 'key', 'string',  'version', 'is_standard')
#         read_only_fields = ('version', 'is_standard')
#
#     def get(self, request, key, format=None):
#         inchi = self.get_object(key=key)
#         serializer = InchiSerializer(inchi)
#         return Response(serializer.data)


class InchiSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='inchi-detail', format='html')

    class Meta:
        model = Inchi
        fields = ('url', 'string', 'key', 'version', 'is_standard')
        read_only_fields = ('version', 'is_standard')

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='organization-detail', format='html')
    #_uid = serializers.UUIDField(source='uid', read_only=True)

    class Meta:
        model = Organization
        fields = ('parent', 'name', 'abbreviation', 'url', 'added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='publisher-detail', format='html', )
    #uid = serializers.UUIDField(source='uid', read_only=True)
    organization = serializers.HyperlinkedRelatedField(queryset=Organization.objects.all(), view_name='organization-detail',)

    class Meta:
        model = Publisher
        fields = ('parent', 'organization', 'name', 'group', 'contact', 'url', 'added', 'modified')

    def create(self, validated_data):
        publisher = Publisher.create(**validated_data)
        publisher.save()
        return publisher


class UrlEntryPointSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='urlentrypoint-detail', format='html', )
    #uid = serializers.UUIDField(source='uid', read_only=True)
    publisher = serializers.HyperlinkedRelatedField(queryset=Publisher.objects.all(), view_name='publisher-detail',)

    class Meta:
        model = UrlEntryPoint
        fields = ('publisher', 'url', 'description', 'is_inchi_resolver')

    def create(self, validated_data):
        entrypoint = UrlEntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class UriEndPointSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='uriendpoint-detail', format='html', )
    #uid = serializers.UUIDField(source='uid', read_only=True)
    entrypoint = serializers.HyperlinkedRelatedField(queryset=UrlEntryPoint.objects.all(), view_name='urlentrypoint-detail')

    class Meta:
        model = UriEndPoint
        fields = ('entrypoint', 'uri', 'description', 'media_type')

    def create(self, validated_data):
        endpoint = UriEndPoint.create(**validated_data)
        endpoint.save()
        return endpoint
