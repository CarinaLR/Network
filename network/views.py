import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    return render(request, "network/index.html")


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
    return render(request, "network/profile.html")

# Connect to /following route


def following(request, username):
    return render(request, "network/following.html")

# Connect to /posts route


@login_required
def posts(request):
    # Set variables and current values
    username = request.user
    # Get a user instance
    user = get_object_or_404(User, username=username)
    content = request.POST.get("content")
    post = request.POST.get("post")
    if request.method == 'POST':
        if post:
            # Get new content for post
            new_content = request.POST.get("content")
            # Get content and save as post, passing new content and user instance.
            post = Post.objects.create(username=user, content=new_content)
            post.save()
            print("post_id ->", post.id)
            print("post ->", post.content)
            print("user -> post ->", post.username)
            return render(request, "network/all_posts.html", {
                "username": post.username,
                "content": post.content
            })
    return render(request, "network/all_posts.html", {
        "username": username,
    })


@login_required
def post(request, post_id):
    # queryset = User.objects.all()
    # print("queryset ->", queryset)

    # Query for requested post
    # try:
    #     post = Post.objects.get(username=request.user, pk=post_id)
    # except Post.DoesNotExist:
    #     return JsonResponse({"error": "Post not found."}, status=404)

    # # Return post contents
    # if request.method == "GET":
    posts = Post.objects.filter(pk=post_id)

    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

    # Post must be via GET or PUT
    # else:
    # return JsonResponse({
    #     "error": "GET or PUT request required."
    # }, status=400)
    # return HttpResponseRedirect(reverse("index"))


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
