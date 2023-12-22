import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *


def index(request):
    return render(request, "network/index.html", {"type": "all"})

def following(request):
    return render(request, "network/index.html", {"type": "following"})

def editPost (request, postID):
    data = json.loads(request.body)
    post = Post.objects.get(id=postID)
    post.content = data.get("content")
    post.save()
    return JsonResponse({"message": "Post Edited"}, status=201)


def follow(request, username):
    targetUser = User.objects.get(username=username)
    follow = Follower(
        user = request.user,
        followTarget = targetUser
    )
    follow.save()
    return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

def unfollow(request, username):
    targetUser = User.objects.get(username=username)
    unfollowTarget = Follower.objects.get(user = request.user, followTarget = targetUser)
    unfollowTarget.delete()
    return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

def profile(request, username):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    user = User.objects.get(username=username)
    userPosts = user.posts.all().order_by("-timestamp").all()
    userFollowersNames = []
    for follower in user.followers.all():
        userFollowersNames.append(follower.user.username)
    currentUserFollows = False
    if request.user.username in userFollowersNames:
        currentUserFollows = True
    followersNumber = len(user.followers.all())
    followsNumber = len(user.follows.all())
    return render(
        request,
        "network/profile.html",
        {
            "currentUserFollows": currentUserFollows,
            "profileName": username,
            "userPosts": userPosts,
            "followersNumber": followersNumber,
            "followsNumber": followsNumber,
        },
    )


def newPost(request):
    data = json.loads(request.body)
    newPost = Post(user=request.user, content=data.get("content"))
    newPost.save()
    return JsonResponse({"message": "New Post created"}, status=201)


def allPosts(request):
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def like(request, postID):
    post = Post.objects.get(id=postID)
    like = Like(user=request.user, post=post)
    like.save()
    return JsonResponse({"message": "Post liked"}, status=201)


def unlike(request, postID):
    post = Post.objects.get(id=postID)
    postLikes = post.likes.all()
    likeToRemove = 0
    for like in postLikes:
        if like.user == request.user:
            likeToRemove = like
            break
    likeToRemove.delete()
    return JsonResponse({"message": "Post unliked"}, status=201)


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
