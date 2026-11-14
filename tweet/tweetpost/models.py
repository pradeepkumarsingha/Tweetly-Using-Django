from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=100)
    photo=models.ImageField(upload_to='photos/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'

class Like(models.Model):
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post=models.ForeignKey(
        tweet,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(
            fields=['user','post'],
            name='uniqe_user_post_like'
            )
        ]
    def __str__(self):
        return f'{self.user.username} liked the post of {self.post_id}'

class Comment(models.Model):
    user=models.ForeignKey(
        User,
            on_delete=models.CASCADE,
            related_name="comments"
    )
    post=models.ForeignKey(
        tweet,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content=models.TextField(max_length=100)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}:{self.content[:30]}"

    
