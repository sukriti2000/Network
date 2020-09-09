from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_posts",default="")
	post=models.CharField(max_length=1000)
	date_time=models.DateTimeField(auto_now_add=True)

class Like(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_likes",default="")	
	post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_liked",default="")

class Followers(models.Model):
	person=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_followers",default="")
	follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_following",default="") 

