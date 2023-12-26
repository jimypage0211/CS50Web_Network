import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *

#View for all posts
def index(request):
    return render(request, "network/index.html", {"type": "all"})

#View for following posts
def following(request):
    return render(request, "network/index.html", {"type": "following"})

#API return for fetching following posts
def followingPosts(request):
    #get all users the actual user follows
    follows = request.user.follows.all()
    followingUsers = []
    for follow in follows:
        followingUsers.append(follow.followTarget)
    #get the posts for that users
    followingUsersPosts = []
    for followingUser in followingUsers:
        followingUsersPosts.extend(followingUser.posts.all())    
    #sorting by id = sorting by timestamps    
    def byID (post):
        return post.id    
    #pagintion
    followingUsersPosts.sort(key=byID, reverse=True)
    paginator = Paginator(followingUsersPosts, 10)
    page = request.GET.get("page")
    postsFromPage = paginator.get_page(page)
    lastPage = False
    if not postsFromPage.has_next():
        lastPage = True
    followingPosts = [post.serialize() for post in postsFromPage]
    return JsonResponse({"posts": followingPosts, "lastPage": lastPage})

#API call for saving an edited post
def editPost (request, postID):
    data = json.loads(request.body)
    post = Post.objects.get(id=postID)
    post.content = data.get("content")
    post.save()
    return JsonResponse({"message": "Post Edited"}, status=201)

#Logic for requesting a follow 
def follow(request, username):
    targetUser = User.objects.get(username=username)
    follow = Follower(
        user = request.user,
        followTarget = targetUser
    )
    follow.save()
    return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

#Logic for requesting an unfollow 
def unfollow(request, username):
    targetUser = User.objects.get(username=username)
    unfollowTarget = Follower.objects.get(user = request.user, followTarget = targetUser)
    unfollowTarget.delete()
    return HttpResponseRedirect(reverse("profile", kwargs={"username": username}))

#View for displaying a profile
def profile(request, username):
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse("login"))
    user = User.objects.get(username=username)
    #get users post sorted by timeStamps
    userPosts = user.posts.all().order_by("-timestamp").all()
    #pagination
    paginator = Paginator(userPosts,10)
    page = request.GET.get('page')
    postsFromPage = paginator.get_page(page)
    userFollowersNames = []
    #saving all followers usernames to check if current user is a follower
    for follower in user.followers.all():
        userFollowersNames.append(follower.user.username)
    currentUserFollows = False
    if request.user.username in userFollowersNames:
        currentUserFollows = True
    #get all user follows and followers count
    followersNumber = len(user.followers.all())
    followsNumber = len(user.follows.all())
    return render(
        request,
        "network/profile.html",
        {
            "currentUserFollows": currentUserFollows,
            "profileName": username,
            "userPosts": userPosts,
            "postsFromPage": postsFromPage,
            "followersNumber": followersNumber,
            "followsNumber": followsNumber,
        },
    )

#API call for saving a new post
def newPost(request):
    data = json.loads(request.body)
    newPost = Post(user=request.user, content=data.get("content"))
    newPost.save()
    return JsonResponse({"message": "New Post created"}, status=201)

#API return for fetching all posts
def allPosts(request):
    #get all post ordered by id 
    posts = Post.objects.all().order_by("-id")
    #pagination
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    postsFromPage = paginator.get_page(page)
    lastPage = False
    if not postsFromPage.has_next():
        lastPage = True
    allPosts = [post.serialize() for post in postsFromPage]
    return JsonResponse({"posts": allPosts, "lastPage": lastPage})

#API call for liking to a post
def like(request, postID):
    post = Post.objects.get(id=postID)
    like = Like(user=request.user, post=post)
    like.save()
    return JsonResponse({"message": "Post liked"}, status=201)

#API call for unliking to a post
def unlike(request, postID):
    post = Post.objects.get(id=postID)
    postLikes = post.likes.all()
    #check if user like this this post
    likeToRemove = None
    for like in postLikes:
        if like.user == request.user:
            likeToRemove = like
            break
    likeToRemove.delete()
    return JsonResponse({"message": "Post unliked"}, status=201)

#View for logging in
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

#View for logging out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#View for registering  new user
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
