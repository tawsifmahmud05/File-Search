from rest_framework import generics, mixins
from .models import Cluster, Url, File
from rest_framework.response import Response
from rest_framework.views import APIView


from .documents import *
from .serializers import *

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,)

from rest_framework.permissions import IsAuthenticated


class ClusterAPI(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Cluster.objects.all()
    serializer_class = clusterSerializer
    name = 'cluster-list'

    filter_fields = (
        'owner',
        'name',
        'crawled',
    )


class FileDocumentView(DocumentViewSet):
    # permission_classes = (IsAuthenticated,)
    document = FileDocument
    serializer_class = FileDocumentSerializer
    lookup_field = 'first_name'
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]

    search_fields = (

        'content',
    )
    multi_match_search_fields = (

        'content',
    )
    filter_fields = {
        'id': 'id',
        'mainurl': 'mainurl',
        'fileurl': 'fileurl',
        'filetype': 'filetype',
        'content': 'content',
        'filecluster': 'filecluster',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id',)
