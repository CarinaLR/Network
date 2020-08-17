import json
from django.forms.models import model_to_dict
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    username = models.ForeignKey(
        "User", default=1, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        'User', default=None, blank=True, related_name='likes')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes
        }

    @property
    def count_likes(self):
        return self.likes.all().count()

    def __str__(self, *args, **kwargs):
        return self.content


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    userpost = models.ForeignKey('Post', on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default=' Like ', max_length=10)

    def _str_(self):
        return str(self.userpost)


class Follow(models.Model):
    following = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='to_follow')
