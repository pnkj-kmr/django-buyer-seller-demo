from django.db import models


class Posts(models.Model):

    id = models.AutoField(primary_key=True)
    post = models.CharField(max_length=8000)
    username = models.CharField(max_length=255)
    usertype = models.CharField(max_length=255, default='Buyer')
    like = models.IntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):

    id = models.AutoField(primary_key=True)
    postid = models.ForeignKey(Posts, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    comment = models.CharField(max_length=2000)


class PostMap(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    postid = models.IntegerField()

    
class CommentMap(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    username2 = models.CharField(max_length=255)


