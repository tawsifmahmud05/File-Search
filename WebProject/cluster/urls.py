from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

from .views import *

from cluster.api import ClusterAPI, FileDocumentView

app_name = 'cluster'

urlpatterns = [

    path('', indexView, name="Index"),
    path('cluster/', cluster_list, name="cluster"),
    path('addCluster/', create_cluster_with_urls, name="addCluster"),
    path('search/', searchPageView, name="search"),

    path('api/clusterlist/', ClusterAPI.as_view()),
    path('api/file/', FileDocumentView.as_view({'get': 'list'})),




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
