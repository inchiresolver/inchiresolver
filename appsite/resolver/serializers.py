from rest_framework import serializers


from resolver.models import Inchi, Organization, Publisher, UrlEntryPoint, UriEndPoint


class InchiSerializer(serializers.HyperlinkedModelSerializer):

    _self = serializers.HyperlinkedIdentityField(view_name='inchi-detail', format='html')
    _uid = serializers.UUIDField(source='uid', read_only=True)

    class Meta:
        model = Inchi
        fields = ('_uid', '_self', 'string', 'key', 'version', 'is_standard')
        read_only_fields = ('version', 'is_standard')

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi
        

        
class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    _self = serializers.HyperlinkedIdentityField(view_name='organization-detail', format='html')
    _uid = serializers.UUIDField(source='uid', read_only=True)

    class Meta:
        model = Organization
        fields = ('_uid', '_self', 'parent', 'name', 'abbreviation', 'url', 'added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    _self = serializers.HyperlinkedIdentityField(view_name='publisher-detail', format='html', )
    _uid = serializers.UUIDField(source='uid', read_only=True)
    organization = serializers.HyperlinkedRelatedField(queryset=Organization.objects.all(), view_name='organization-detail',)

    class Meta:
        model = Publisher
        fields = ('_uid', '_self', 'parent', 'organization', 'name', 'group', 'contact', 'url', 'added', 'modified')

    def create(self, validated_data):
        publisher = Publisher.create(**validated_data)
        publisher.save()
        return publisher


class UrlEntryPointSerializer(serializers.HyperlinkedModelSerializer):

    _self = serializers.HyperlinkedIdentityField(view_name='urlentrypoint-detail', format='html', )
    _uid = serializers.UUIDField(source='uid', read_only=True)
    publisher = serializers.HyperlinkedRelatedField(queryset=Publisher.objects.all(), view_name='publisher-detail',)

    class Meta:
        model = UrlEntryPoint
        fields = ('_uid', '_self', 'publisher', 'url', 'description', 'is_inchi_resolver')

    def create(self, validated_data):
        entrypoint = UrlEntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class UriEndPointSerializer(serializers.HyperlinkedModelSerializer):

    _self = serializers.HyperlinkedIdentityField(view_name='uriendpoint-detail', format='html', )
    _uid = serializers.UUIDField(source='uid', read_only=True)
    entrypoint = serializers.HyperlinkedRelatedField(queryset=UrlEntryPoint.objects.all(), view_name='urlentrypoint-detail')

    class Meta:
        model = UriEndPoint
        fields = ('_uid', '_self', 'entrypoint', 'uri', 'description', 'media_type')

    def create(self, validated_data):
        endpoint = UriEndPoint.create(**validated_data)
        endpoint.save()
        return endpoint
