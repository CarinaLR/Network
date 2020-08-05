
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("posts/<str:userposts>", views.userposts, name="userposts"),
    path("following/<str:username>", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow_profile/<int:post_id>",
         views.follow_profile, name="follow_profile")
]
