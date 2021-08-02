from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import ListField
from rest_framework_recursive.fields import RecursiveField

from account.serializers import UserSerializer
from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    likes = serializers.StringRelatedField(many=True, read_only=True)
    replies = serializers.ListSerializer(child=RecursiveField(replies=True))

    class Meta:
        model = Comment
        exclude = []

    def __init__(self, *args, **kwargs):
        if 'replies' in kwargs:
            replies = kwargs['replies']
            if replies is False:
                self.fields.pop("replies")
            del kwargs['replies']
        else:
            self.fields.pop("replies")
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        if "reply_to" not in validated_data:
            validated_data["reply_to"] = None
        else:
            try:
                Comment.objects.get(pk=validated_data["reply_to"].id, post=validated_data["post"])
            except:
                raise serializers.ValidationError({"error": "Post and replying comment does not match."})

        comment = validated_data["post"].comments.create(
            writer=validated_data["writer"],
            text=validated_data["text"],
            reply_to=validated_data["reply_to"]
        )

        return comment


class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)
    pub_date = serializers.DateTimeField(default=datetime.now)
    tags = ListField(
        child=serializers.CharField(), write_only=True
    )
    likes = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

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
