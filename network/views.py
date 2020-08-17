import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow


def index(request):
    # Set variables and current values
    username = request.user
    # Get querySet for all posts, with the most recent posts first.
    all_post = Post.objects.order_by("-timestamp").all()
    # Get a user instance
    user = get_object_or_404(User, username=username)
    content = request.POST.get("content")
    post = request.POST.get("post")
    # Show 10 posts per page.
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    follow = request.POST.get("follow_profile")
    current_user = request.user
    if request.method == 'POST':
        if post:
            # Get new content for post
            new_content = request.POST.get("content")
            # Get content and save as post, passing new content and user instance.
            post = Post.objects.create(username=user, content=new_content)
            post.save()
            return render(request, "network/index.html", {
                "username": post.username,
                "content": post.content,
                "posts": all_post,
                "page_obj": page_obj
            })
        # Activate button to save followers and following.
        if follow:
            post_username = request.POST.get("follow_profile")

    return render(request, "network/index.html", {
        "posts": all_post,
        "page_obj": page_obj
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
    print("reach profile page")
    # Get querySet for all posts, with the most recent posts first.
    all_post = Post.objects.order_by("-timestamp").all()
    user = request.user

    profile_user = get_object_or_404(User, username=username)

    # Get querySet for user posts, with the most recent posts first.
    posts = Post.objects.filter(
        username=profile_user).order_by("-timestamp").all()
    post_list = len(posts)

    # Get length of querySet for all followers, indicator of how many followers the user has.
    followers = Follow.objects.filter(follower=profile_user)
    followers_list = len(followers)

    # Get length of querySet for all following, indicator of how many users the user follows.
    following = Follow.objects.filter(following=profile_user)
    following_list = len(following)

    # Get length of querySet for follows between users.
    follows = Follow.objects.filter(
        following=user, follower=profile_user)

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
    if request.method == 'GET':
        username = get_object_or_404(User, username=username)
        print("user ->", username)
        follows = Follow.objects.filter(follower=username)

        # Get querySet for all posts, with the most recent posts first.
        posts = Post.objects.order_by("-timestamp").all()

        posts_to_follow = []

        for post in posts:
            for follower in follows:
                if follower.following == post.username:
                    posts_to_follow.append(post)

        # Iterate over appended posts

        for posts_i in posts_to_follow:
            posti_id = posts_i.id
            for post_j in posts_to_follow:
                postj_id = post_j.id
                count = 1
                if posti_id == postj_id:
                    count += 1
                if count > 1:
                    posts_to_follow.remove(post_j)

        # Show 10 posts per page.
        paginator = Paginator(posts_to_follow, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if not follows:
            return render(request, 'network/following.html', {'message': "Could be a good idea to start to follow people of your interest!"})

    return render(request, "network/following.html", {
        "posts": posts_to_follow,
        "page_obj": page_obj
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
    # Show 10 posts per page.
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        "all_posts": all_posts,
        "page_obj": page_obj
    })


@login_required
def post(request, post_id):
    print("reach post page")
    queryset = Post.objects.all()
    username = request.user
    # Query for requested post
    try:
        post = Post.objects.get(username=username, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        post_id = post.id
        post_username = post.username
        post_content = post.content
        post_timestamp = post.timestamp
        response = {"post_id": post_id,
                    "post_content": post_content, "post_timestamp": post_timestamp}

        for post in queryset:
            if post.id == post_id:
                return JsonResponse(response, safe=False)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

    return HttpResponseRedirect(reverse("index"))


def userposts(request, userposts):
    print("reach-userpost")
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
    print("reach follow_profile page")
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

    following = Follow.objects.filter(follower=current_user)

    follows = Follow.objects.filter(
        follower=current_user, following=owner_post)
    total_follower = len(follower)

    total_following = len(following)

    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def edit_post(request, post_id):
    print("i'm here, post_id", post_id)

    # Get post by id.
    get_post = Post.objects.get(pk=post_id)

    # Block to handle PUT request.
    if request.method == "PUT":
        print("pass request PUT")
        # Get data from fetch, update content and save.
        data = json.loads(request.body)
        get_post.content = data["content"]
        get_post.save()
    return HttpResponse(status=204)


def like_post(request, post_id):
    print("reach like_post in views")
    # Set user variables.
    user = request.user
    post = Post.objects.get(pk=post_id)

    # Return post contents
    if request.method == "GET":
        post_id = post.id
        post_username = post.username
        post_content = post.content
        post_timestamp = post.timestamp
        response = {"post_id": post_id,
                    "post_content": post_content, "post_timestamp": post_timestamp}
        return JsonResponse(response, safe=False)

    # Block to handle POST request.
    if request.method == "POST":
        post_obj = Post.objects.get(pk=post_id)

        # Block to handle user in post if remove or add.
        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)

        like, created = Like.objects.get_or_create(
            userpost_id=post_id, user=user)
        # Change values for like object.
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"

        like.save()
        return HttpResponseRedirect(reverse("index"))
