from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import userSerializer, emailSerializer
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated


# class UserAPI(APIView):

#     def get(self, request):
#         articles = User.objects.all()
#         serializer = userSerializer(articles, many=True)
#         return Response(serializer.data)

class UserAPI(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = userSerializer
    name = 'user-list'

    filter_fields = (
        'email',
        'id',
    )
