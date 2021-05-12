from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [

    path("login/", views.login, name = "login"),
    path("signup/", views.signup, name="signup"),
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("profile/update", views.profileUpdate, name="profileUpdate"),
    path("profile/<pk>", views.profile, name="profile"),
    path("chat/<pk>", views.chat, name= "chat"),
    path("account/change_password/", views.changePassword, name="changePassword"),
    path("account/delete_account/", views.deleteAccount, name="deleteAccount"),
    path("account/change_mail/", views.changeMail, name="changeMail"),
    path("reset_password/", views.resetPassword, name="resetPassword"),
    path("get_message/<pk>", views.getMessage, name="getMessage"),
    path("send_message/<pk>", views.sendMessage, name="sendMessage"),

]



