from datetime import date
from django.db import models


class User(models.Model):
    userName = models.CharField(max_length=18)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=12)


class Blog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=16)
    postDetail = models.CharField(max_length=10000)
    postDate = models.DateField(default=date.today)
    publisherName = models.CharField(max_length=16)

class Comment(models.Model):
    messages=models.CharField('messages',max_length=10000)
    dateComment=models.DateField(default=date.today)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
