from rest_framework import serializers

from .models import WebResourceType, WebResource


class WebResourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebResourceType
        fields = ('id', 'name', 'description',)
        # read_only_fields = ('xyz', )


class WebResourceTypeHLMSerializer(serializers.HyperlinkedModelSerializer):
    # customfbv1 = serializers.HyperlinkedIdentityField(view_name='webresourcetype-customfbv1')
    # customfbv2html = serializers.HyperlinkedIdentityField(view_name='webresourcetype-customfbv2html', format='html')

    class Meta:
        model = WebResourceType
        fields = ('id', 'name', 'description')
        # fields = fields + ('customfbv1', 'customfbv2html')
        # fields = (fields[0],) + ('url',) + fields[1:]  # insert the url field at index 1
        fields = ('url',) + fields  # prepend the url field
        # fields = fields[1:]  # strip the first field (id)


class WebResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebResource
        fields = ('id', 'name', 'description', 'resource_type', 'uri')
        # read_only_fields = ('xyz', )


class WebResourceHLMSerializer(serializers.HyperlinkedModelSerializer):
    resource_type__name = serializers.ReadOnlyField(source='resource_type.name')

    class Meta:
        model = WebResource
        fields = ('id', 'name', 'description', 'resource_type', 'uri')
        fields = fields + ('resource_type__name',)  # append fields
        # fields = (fields[0],) + ('url',) + fields[1:]  # insert the url field at index 1
        fields = ('url',) + fields  # prepend the url field
        # fields = fields[1:]  # strip the first field (id)
