from django.contrib import admin

# Register your models here.
from .models import Url, Cluster, File


admin.site.register(Url)
admin.site.register(Cluster)
admin.site.register(File)
