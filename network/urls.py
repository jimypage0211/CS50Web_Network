
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    
    #API calls
    path("editPost/<int:postID>", views.editPost, name="editpost"),
    path("newPost", views.newPost, name="newPost"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("following/<str:username>", views.following, name="following"),
    path("like/<int:postID>", views.like, name="like"),
    path("unlike/<int:postID>", views.unlike, name="unlike")
]
