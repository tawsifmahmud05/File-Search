from django_elasticsearch_dsl import (Document, fields, Index,)
from .models import File


FILE_INDEX = Index('file')

FILE_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@FILE_INDEX.doc_type
class FileDocument(Document):

    id = fields.IntegerField(attr='id')

    fielddata = True

    mainurl = fields.TextField(
        fields={
            'raw': {
                'type': 'text',

            }
        },
    )
    filecluster = fields.TextField(
        fields={
            'raw': {
                'type': 'text',

            }
        },
    )

    fileurl = fields.TextField(
        fields={
            'raw': {
                'type': 'text',

            }
        },
    )

    content = fields.TextField(
        fields={
            'raw': {
                'type': 'text',

            }
        },
    )

    class Django(object):
        model = File
