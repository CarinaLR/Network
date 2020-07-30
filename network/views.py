from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
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


def profile(request):
    return HttpResponseRedirect(reverse("index"))

# Connect to /following route


def following(request):
    return HttpResponseRedirect(reverse("index"))

# Connect to /posts route


@login_required
def posts(request):
    # Get current user info
    username = request.user.username
    print("username", username)
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        content = request.POST["content"]
        try:
            post = Post.objects.create(content=content, username=user)
            post.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            pass
    else:
        return render(request, "network/all_posts.html", {
            "username": username,
        })
