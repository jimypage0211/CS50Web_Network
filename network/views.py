import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *


def index(request):    
    return render(request, "network/index.html")

def newPost(request):
    body = request.POST["body"]
    newPost = Post(
        user = request.user,
        content = body.get('content')    
        )
    newPost.save()
    return JsonResponse({"message": "New Post created"}, status=201)
    
def allPosts(request):    
    posts = Post.objects.all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def like (request, postID):
    post = Post.objects.get(id=postID)
    like = Like(
        user = request.user,
        post = post
    )
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




"""
multiple pages method

 if request.method == "POST":
        content = request.POST["postContent"]
        post = Post(
            user = request.user,
            content = content,            
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))   
    else:
        posts = Post.objects.all()
        return render(request, "network/index.html", {"posts": posts}) 
        

    index.html:
    <div id="newPost">
        <form action="{% url 'index' %}" method="Post">
            {% csrf_token %}
            <textarea name="postContent" id="postContent" cols="30" rows="10"></textarea>
            <input type="submit" value="Post">
        </form>
    </div>
    <div id="allPost">
        {% for post in posts  %}
            <div>{{post}}</div>
        {% endfor %}
    </div>
        
    
    script tag:
    src="{% static 'network/inbox.js' %}"
"""