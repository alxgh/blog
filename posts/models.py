import json
from typing import List

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    digest = models.TextField(max_length=500)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.TextField()
    pub_date = models.DateTimeField()

    def set_tags(self, tags: List[str]):
        self.tags = json.dumps(tags)

    def get_tags(self) -> List[str]:
        try:
            return json.loads(self.tags)
        except:
            return []

    class Meta:
        ordering = ['-id']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_likes'

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_likes'

    def __str__(self):
        return self.user.username
