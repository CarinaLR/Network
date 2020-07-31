import json
from django.forms.models import model_to_dict
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.db import models


class User(AbstractUser):
    pass


class PostSerializer(models.Manager):
    def get_posts(self, *args, **kwargs):
        return self.all()

    def get_post(self, post_id, *args, **kwargs):
        return get_object_or_404(self, id=post_id)

    def get_user_posts(self, username, *args, **kwargs):
        return self.filter(username=username)

    def get_user_post(self, post_id, user, *args, **kwargs):
        return get_object_or_404(self, pk=post_id, username=user)


class Post(models.Model):
    username = models.ForeignKey(
        "User", default=1, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        'User', default=None, blank=True, related_name='likes')

    objects = PostSerializer()

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes.all().count()
        }

    def __str__(self, *args, **kwargs):
        return self.content


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    userpost = models.ForeignKey('Post', on_delete=models.CASCADE)


class Follow(models.Model):
    following = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='to_follow')
