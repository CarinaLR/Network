import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    # Get querySet for all posts, with the most recent posts first.
    all_post = Post.objects.order_by("-timestamp").all()
    follow = request.POST.get("follow_profile")
    current_user = request.user
    # Activate button to save followers and following.
    if request.method == "POST":
        if follow:
            post_username = request.POST.get("follow_profile")

    return render(request, "network/index.html", {
        "posts": all_post
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Connect to /profile route


def profile(request, username):
    # Get querySet for all posts, with the most recent posts first.
    all_post = Post.objects.order_by("-timestamp").all()
    user = request.user
    profileuser = get_object_or_404(User, username=username)
    # Get querySet for user posts, with the most recent posts first.
    posts = Post.objects.filter(
        username=profileuser).order_by("-timestamp").all()
    post_list = len(posts)
    # Get length of querySet for all followers, indicator of how many followers the user has.
    followers = Follow.objects.filter(follower=profileuser)
    followers_list = len(followers)
    print("followers", followers)
    # Get length of querySet for all following, indicator of how many users the user follows.
    following = Follow.objects.filter(following=profileuser)
    following_list = len(following)
    print("following", following)
    # Get length of querySet for follows between users.
    follows = Follow.objects.filter(
        following=user, follower=profileuser)

    return render(request, "network/profile.html", {
        "user": user,
        "userPost": posts,
        "followers": followers_list,
        "following": following_list,
        "posts_list": post_list,
        "follows": follows
    })

# Connect to /following route


@login_required
def following(request, username):
    # # Get querySet for all posts, with the most recent posts first.
    # all_post = Post.objects.order_by("-timestamp").all()

    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        print("user ->", user)
        follows = Follow.objects.filter(follower=user)
        print("follows ->", follows)
        posts = Post.objects.order_by("-timestamp").all()
        print("posts ->", posts)
        posted = []
        for post in posts:
            for follower in follows:
                if follower.following == post.user:
                    posted.append(post)
        print("posted ->", posted)
        if not follows:
            return render(request, 'network/following.html', {'message': "Could be a good idea to start to follow people of your interest!"})

    return render(request, "network/following.html", {
        "posts": posted
    })


# Connect to /posts route


@login_required
def posts(request):
    # Set variables and current values
    username = request.user
    # Get a user instance
    user = get_object_or_404(User, username=username)
    content = request.POST.get("content")
    post = request.POST.get("post")
    all_posts = Post.objects.order_by("-timestamp").all()
    if request.method == 'POST':
        if post:
            # Get new content for post
            new_content = request.POST.get("content")
            # Get content and save as post, passing new content and user instance.
            post = Post.objects.create(username=user, content=new_content)
            post.save()
            return render(request, "network/all_posts.html", {
                "username": post.username,
                "content": post.content,
                "all_posts": all_posts
            })
    return render(request, "network/all_posts.html", {
        "username": username,
        "all_posts": all_posts
    })


@login_required
def post(request, post_id):
    queryset = Post.objects.all()
    print("queryset ->", queryset)

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        print("post_id ->", post.id)
        print("post ->", post.content)
        print("user -> post ->", post.username)
        # return JsonResponse(queryset.serialize())

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

    return HttpResponseRedirect(reverse("index"))


def userposts(request, userposts):
    # Filter post returned based on userposts
    if userposts == "userposts":
        posts = Post.objects.filter(
            username=request.user, content=request.user
        )
    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.get_posts() for post in posts], safe=False)

    return render(request, "network/index.html")


def follow_profile(request, post_id):
    # Set variables for current user
    current_user = request.user
    # Set variables for user post
    post = Post.objects.get(pk=post_id)
    user_post = post.username
    owner_post = get_object_or_404(User, username=user_post)
    # Set variables for follows, create object and save it
    follow = Follow.objects.create(
        following=current_user, follower=owner_post)
    follow.save()
    follower = Follow.objects.filter(following=current_user)
    print("follower ->", follower)
    following = Follow.objects.filter(follower=current_user)
    print("following ->", following)
    follows = Follow.objects.filter(
        follower=current_user, following=owner_post)
    total_follower = len(follower)
    print("total_follower ->", total_follower)
    total_following = len(following)
    print("total_following ->", total_following)

    return HttpResponseRedirect(reverse("index"))
