from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import ListField

from account.serializers import UserSerializer
from posts.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(default=datetime.now)
    tags = ListField(
        child=serializers.CharField(), write_only=True
    )
    likes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        exclude = []

    def to_representation(self, instance: Post) -> Post:
        ret = super().to_representation(instance)
        ret["tags"] = instance.get_tags()

        return ret

    def create(self, validated_data) -> Post:
        post = Post.objects.create(
            writer_id=validated_data["writer"].id,
            pub_date=validated_data["pub_date"],
            content=validated_data["content"],
            digest=validated_data["digest"],
            title=validated_data["title"]
        )

        post.set_tags(validated_data["tags"])
        post.save()
        return post

    def update(self, instance: Post, validated_data) -> Post:
        super().update(instance, validated_data)
        instance.set_tags(validated_data["tags"])
        instance.save()
        return instance
