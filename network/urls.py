
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #API calls
    path("newPost", views.newPost, name="newPost"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("like/<int:postID>", views.like, name="like"),
    path("unlike/<int:postID>", views.unlike, name="unlike")
]
