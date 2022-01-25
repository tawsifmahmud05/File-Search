from .models import Url, Cluster, File
from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents import *

# user serializers


class urlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = '__all__'

# cluster serializers


class clusterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cluster
        fields = '__all__'

# File serializers


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

#FileDocumentSerializer

class FileDocumentSerializer(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        model = File
        document = FileDocument
        fields = (
            'id',
            'mainurl',
            'fileurl',
            'filetype',
            'content',
            'filecluster',
        )
#Represent location value.
        def get_location(self, obj):

            try:
                return obj.location.to_dict()
            except:
                return {}
