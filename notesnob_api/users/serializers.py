from rest_framework import serializers


class UsersSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers