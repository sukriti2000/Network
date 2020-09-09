
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post",views.add_post,name="add_post"),
    path("profile/<str:username>",views.profile,name="profile"),
    path("add_follower/<int:user_id>",views.add_follower,name="add_follower"),
    path("update_follower/<int:user_id>",views.update_follower,name="update_follower"),
    path("updatePost/<int:user_id>/<str:newpost>",views.updatePost,name="updatePost"),
    path("add_like/<int:post_id>",views.add_like,name="add_like"),
    path("following",views.following,name="following")
]
