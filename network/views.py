from django.contrib.auth import authenticate, login, logout 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User,Post,Like,Followers


def index(request):
    All_post=Post.objects.all()
    All_post=All_post.order_by("-date_time").all()
    paginator=Paginator(All_post,10)
    page=request.GET.get('page')
    All_post=paginator.get_page(page)
    user = authenticate(request, username=request.user)
    if user is not None: 
        lists=[]
        my_likes=Like.objects.filter(user=request.user)
        for posts in my_likes:
            lists.append(posts.post.id)
    else:
        lists=[]
    return render(request, "network/index.html",{
        "All_post":All_post,"lists":lists
       })


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

def add_post(request):
    if request.method == "POST":
        post=request.POST["post_added"]
        username=request.user
        instance=Post(post=post,user=username)
        instance.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request,username):
    current=User.objects.get(username=username)
    user_post=Post.objects.filter(user=current)
    user_post=user_post.order_by("-date_time").all()
    check=Followers.objects.filter(person=current).filter(follower=request.user).count()
    follower_count=Followers.objects.filter(person=current).count()
    following_count=Followers.objects.filter(follower=current).count()
    return render(request,"network/profile.html",{
        "current":current,"user_post":user_post,"check":check,"follower_count":follower_count,"following_count":following_count
        })
      
def add_follower(request,user_id):
    user_info=User.objects.get(pk=user_id);
    check=Followers.objects.filter(person=user_info).filter(follower=request.user).first()
    if check is None:
        instance=Followers(person=user_info,follower=request.user)
        instance.save()
        return HttpResponse("followed")
    else:
        check.delete()
        return HttpResponse("Removed")

def update_follower(request,user_id):
    person=User.objects.get(pk=user_id)
    follower_count=person.my_followers.count()
    return HttpResponse(follower_count) 

def updatePost(request,user_id,newpost):
    instance=Post.objects.get(pk=id)
    instance.post=newpost
    instance.save()
    return HttpResponseRedirect(reverse("index"))

def add_like(request,post_id):
    user=request.user
    post=Post.objects.get(pk=post_id)
    check=Like.objects.filter(post=post).filter(user=user).first()
    if check is None:
        instance=Like(post=post,user=user)
        instance.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        check.delete()
        return HttpResponseRedirect(reverse("index"))

def following(request):
    posts=Post.objects.all()
    posts=posts.order_by("-date_time").all()
    me_following=Followers.objects.filter(follower=request.user)
    me_following_list=[]
    for follower in me_following:
        me_following_list.append(follower.person)
    all_posts=[]
    for post in posts:
        if post.user in me_following_list:
            all_posts.append(post)
    paginator=Paginator(all_posts,10)
    page=request.GET.get('page')
    all_posts=paginator.get_page(page)
    like_by_me=Like.objects.filter(user=request.user)
    my_likes=[]
    for this_post in like_by_me:
        my_likes.append(this_post.post.id)
    return render(request,"network/following.html",{
        "all_post":all_posts,"my_likes":my_likes
        })

