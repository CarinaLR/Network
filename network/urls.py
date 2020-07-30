
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
    path("following/<str:username>", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile")
]
