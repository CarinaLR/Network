from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    username = models.ForeignKey(
        "User", default=1, on_delete=models.CASCADE, related_name="all_posts")
    sender = models.ForeignKey(
        "User", default=1, on_delete=models.PROTECT, related_name="post_sent")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.post,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes
        }
