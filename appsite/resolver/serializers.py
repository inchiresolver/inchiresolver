from rest_framework_json_api import serializers
#from rest_framework.response import Response
#from rest_framework.reverse import reverse


from resolver.models import Inchi, Organization, Publisher, EntryPoint, EndPoint

class InchiSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Inchi
        fields = ('url', 'string', 'key', 'version', 'is_standard', 'safeopt', 'entrypoints', 'added', 'modified')
        read_only_fields = ('key', 'version', 'is_standard', 'added', 'modified')

    def create(self, validated_data):
        inchi = Inchi.create(**validated_data)
        inchi.save()
        return inchi


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ('url', 'parent', 'name', 'abbreviation', 'website', 'added', 'modified')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        organization = Organization.create(**validated_data)
        organization.save()
        return organization


class PublisherSerializer(serializers.HyperlinkedModelSerializer):

    organization = serializers.HyperlinkedRelatedField(queryset=Organization.objects.all(), view_name='organization-detail',)

    class Meta:
        model = Publisher
        fields = ('url', 'parent', 'organization', 'name', 'group', 'contact', 'url', 'added', 'modified')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        publisher = Publisher.create(**validated_data)
        publisher.save()
        return publisher


class EntryPointSerializer(serializers.HyperlinkedModelSerializer):

    publisher = serializers.HyperlinkedRelatedField(queryset=Publisher.objects.all(), view_name='publisher-detail',)

    class Meta:
        model = EntryPoint
        fields = ('url', 'publisher', 'name', 'description', 'category', 'href')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        entrypoint = EntryPoint.create(**validated_data)
        entrypoint.save()
        return entrypoint


class EndPointSerializer(serializers.HyperlinkedModelSerializer):

    #self = serializers.HyperlinkedIdentityField(view_name='uriendpoint-detail', format='html', )
    #uid = serializers.UUIDField(source='uid', read_only=True)
    entrypoint = serializers.HyperlinkedRelatedField(queryset=EntryPoint.objects.all(), view_name='urlentrypoint-detail')

    class Meta:
        model = EndPoint
        fields = ('url', 'entrypoint', 'description', 'category', 'uri',  'media_type')
        read_only_fields = ('added', 'modified')

    def create(self, validated_data):
        endpoint = EndPoint.create(**validated_data)
        endpoint.save()
        return endpoint
