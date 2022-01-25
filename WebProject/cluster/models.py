# Create your models here.
from django.conf import settings
from django.db import models


class Cluster(models.Model):

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,)
    crawled = models.BooleanField(default=False)

    class Meta:
        db_table = 'Cluster'

    def __str__(self):
        return self.name


class Url(models.Model):

    url = models.CharField(max_length=10000)
    depth = models.CharField(max_length=10000)

    crawling = (
        ('ALL', "ALL"),
        ('DOC', 'DOC'),
        ('PDF', 'PDF'),
        ('PPT', 'PPT'),
        ('HTML', 'HTML'),
        ('NON-HTML', 'NON-HTML'),
    )
    crawling_strategy = models.CharField(max_length=100, choices=crawling)

    cluster = models.ForeignKey(
        Cluster,
        related_name='Urls', on_delete=models.SET_NULL,
        null=True)

    class Meta:
        db_table = 'URL'

    def __str__(self):
        return self.url


class File(models.Model):
    filecluster = models.CharField(max_length=1000, default=0)
    mainurl = models.CharField(max_length=1000)
    fileurl = models.CharField(max_length=10000)
    filetype = models.CharField(max_length=255)
    content = models.TextField(max_length=100000000000000000)

    class Meta:
        db_table = 'File'

    def __str__(self):
        return self.fileurl
