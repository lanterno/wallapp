from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('owner', 'text')
