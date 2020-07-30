from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    username = models.ForeignKey(
        "User", default=1, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.ManyToManyField("User", related_name="post_sent")
    likes = models.ManyToManyField(
        'User', default=None, blank=True, related_name='likes')

    def user_posts(self):
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "sent": [username.post for username in self.sent.all()],
            "likes": self.likes.all().count()
        }


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    userpost = models.ForeignKey('Post', on_delete=models.CASCADE)


class Follow(models.Model):
    following = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='to_follow')
