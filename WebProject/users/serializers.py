from django.contrib.auth.models import User
from rest_framework import serializers


# Serialize Json data
class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

    # Serialize Json data


class emailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
