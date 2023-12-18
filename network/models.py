from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} posted {self.content} on {self.timestamp}"
    
    def serialize(self):
        comments = self.comments.all()
        commentsList = []
        for comment in comments:
            commentsList.append(
                {
                    "comment": comment.commentContent,
                    "user": comment.user.username
                }
            )

        return{
            "id": self.id,
            "username": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [like.user.username for like in self.likes.all()],
            "comments": commentsList
        }


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows")
    followTarget = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    
    def __str__(self) -> str:
        return f"{self.user} follows {self.followTarget}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commentContent= models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{self.user} said {self.commentContent} on {self.post}"
    

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self) -> str:
        return f"{self.user} likes {self.post}"
    
    