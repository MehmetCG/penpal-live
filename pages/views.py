from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django_countries import countries
from django.conf.global_settings import LANGUAGES
from django.core.files.storage import FileSystemStorage
from PIL import Image
import os
from penpal.settings import BASE_DIR, EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_PASSWORD
from django.core.mail import send_mail
import smtplib
from random import randint
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *



def login(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["psw"]
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            user.userprofile.is_online = True
            user.userprofile.last_seen = datetime.now() # it is required for a correct sorting on home page
            user.userprofile.save()
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, "The username or password is incorrect")
            return redirect("login")
    else:
        return render(request, "login.html")






def signup(request):
    if request.method == "POST":
        username = request.POST["uname"]
        email = request.POST["email"]
        password = request.POST["psw"]
        repassword = request.POST["psw-repeat"]

        unavailableNames = ['inbox','chat','account'] #These are part of URL paths and musn't be used

        if password == repassword:
            if User.objects.filter(username = username).exists() or (username in unavailableNames):
                messages.error(request, "This username is unavailable. Please try another.")
                return redirect("signup")
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, "An account already exists for that email")
                    return redirect("signup")
                else:
                    user = User.objects.create_user(username = username, email = email, password = password)
                    user.save()
                    auth.login(request, auth.authenticate(username = username, password = password))                                       

                    #create a message instance from admin to user. New user will be welcomed by this message.
                    admin = User.objects.filter(username = 'Admin').first()
                    messageText = f"Welcome {request.user}! Start to connect with people by searching on home page. Enjoy :)"
                    Message.objects.create(sender = admin  , recipient = request.user, messageText= messageText)
                    LatestMessage.objects.create(messageText=messageText).senders.add(request.user,admin)
                    UnreadMessage.objects.create(sender2=admin, recipient2=request.user)                   
                    messages.success(request, "Your account has been created successfully")
                    send_mail("Welcome to Penpal-Exchange", f"Welcome {username}, we are happy to see you in our comunity!", EMAIL_HOST_USER, [email])
                 
                    return redirect("profileUpdate")
                   
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")
    else:
        return render(request, "signup.html")   






@login_required
def home(request):
    languages = dict(sorted(dict(LANGUAGES).items(), key = lambda item: item[1])).values()  #alphatize dictionary values 
    countriess = dict(countries).values()
    numbers = list(range(101))
    latestSearch = LatestSearch.objects.filter(searcher = request.user).first()

    context = { "countries":countriess, "languages":languages, "numbers":numbers,"latestSearch":latestSearch }
    return render( request, "home.html", context )


def search(request):
    age1 = request.GET["age1"]
    age2 = request.GET["age2"]
    gender = request.GET["gender"]
    country = request.GET["country"]
    nativeLanguage = request.GET["nativeLanguage"]
    practisingLanguage = request.GET["practisingLanguage"]

    LatestSearch.objects.filter(searcher = request.user).update( minAge = age1, maxAge = age2,  gender = gender, 
                        country = country, nativeLanguage = nativeLanguage, practisingLanguage = practisingLanguage )

    profiles = UserProfile.objects.exclude(user = request.user).order_by( "-is_online" , "-last_seen")
    if age1 != 0:
        profiles = profiles.filter(age__gte = age1)
    if age2 != 100:
        profiles = profiles.filter(age__lte = age2)
    if gender != "Both":
        profiles = profiles.filter(gender = gender)
    if country != "All":
        profiles = profiles.filter(country =  country)
    if nativeLanguage != "All":
        profiles = profiles.filter(nativeLanguage = nativeLanguage)
    if practisingLanguage != "All":
        profiles = profiles.filter(practisingLanguage = practisingLanguage)

    serializedFilter = UserProfileSerializer(profiles, many=True)

    return JsonResponse(serializedFilter.data, safe=False)




def logout(request):
    request.user.userprofile.is_online = False
    request.user.userprofile.last_seen = datetime.now()
    request.user.userprofile.save()
    auth.logout(request)
    return redirect("login")





@login_required
def profileUpdate(request):
    languages = dict(sorted(dict(LANGUAGES).items(), key = lambda item: item[1])).values()  #alphatize dictionary values 
    countriess = dict(countries).values()
    profile = UserProfile.objects.filter(user = request.user)
    context = { "profile":profile.first(), "countries":countriess, "languages":languages }
    

    if request.method == "POST": 
        age = request.POST["age"]
        gender = request.POST["gender"]
        country = request.POST["country"]
        description = request.POST["description"]
        nativeLanguage = request.POST["nativeLanguage"]
        practisingLanguage = request.POST["practisingLanguage"]
        image = request.FILES.get("image")
        currentImage = profile.first().image.name

        if image: # Remove the obligation of choosing file each time while updating form
            if currentImage != "default-profile-picture.jpg" :
                imagePath = BASE_DIR +"/media/" + profile.first().image.name
                if os.path.isfile(imagePath): #delete old profile photo if it exists
                    os.remove(imagePath)
                
            filename = FileSystemStorage().save("images/" + request.user.username + "_" + image.name, image)
            profile.update(image = filename)
        
        profile.update( age = age, gender = gender, country = country, description = description,
                        nativeLanguage = nativeLanguage, practisingLanguage = practisingLanguage )
        return redirect("profile", request.user)
    else:
        return render(request, "profileUpdate.html", context)







@login_required
def profile(request, pk):
    viewedUser = User.objects.get(username = pk)
    context = { "profile":viewedUser.userprofile}
    
    return render( request, "profile.html", context )







@login_required
def chat(request, pk):
    otheruser = User.objects.filter(username=pk).first()
    chats = Message.objects.filter(Q(Q(sender=request.user) & Q(recipient=otheruser)) | (Q(sender=otheruser) & Q(recipient=request.user))).order_by("created")
    msgs = request.user.latestmessage_set.all().order_by("-created")
    context = {
        "otheruser" : otheruser,
        "chats" : chats,
        "msgs" : msgs,     
    }
      

    UnreadMessage.objects.filter(sender2=otheruser, recipient2=request.user).all().delete() # Delete all related unread messages when chat is clicked by user

    if request.user.userprofile.gender == "":
        messages.warning(request, "Please complete your profile to send a message!")
        return redirect("profileUpdate")

    if pk=="inbox":
        return render( request, "chat.html", context )
   
    if pk == request.user.username: # to prevent users from sending message to themselves
        return redirect("home")

    if otheruser == None:
        messages.warning(request, "This user doesn't exist")
        return redirect("home")

    return render(request, "chat.html", context)

def sendMessage(request,pk):
    otheruser = User.objects.filter(username=pk).first()
    messagetext = request.GET['messageText']
    message = Message.objects.create(sender = request.user, recipient = otheruser, messageText=messagetext)      
    LatestMessage.objects.filter(senders = request.user).filter(senders = otheruser).delete()
    LatestMessage.objects.create(messageText=messagetext).senders.add(request.user,otheruser)
    UnreadMessage.objects.create(sender2=request.user, recipient2=otheruser)

    serializedMessage = MessageSerializer(message)
    return JsonResponse(serializedMessage.data)





def getMessage(request, pk):
    otheruser = User.objects.filter(username=pk).first()
    UnreadMessage.objects.filter(sender2=otheruser, recipient2=request.user).all().delete()    
    message = Message.objects.filter(recipient=request.user).last()
    
    serializedMessage = MessageSerializer(message)

    return JsonResponse(serializedMessage.data, safe=False)


@login_required
def changePassword(request):
    user = request.user

    if request.method == "POST":
        oldPassword = request.POST["old-psw"]
        newPassword = request.POST["psw"]
        reNewpassword = request.POST["psw-repeat"]
       
        if user.check_password(oldPassword) == False:
            messages.error(request, "Old password is incorrect")
            return redirect("changePassword")
        else:
            if newPassword != reNewpassword:
                messages.error(request, "New passwords do not match")
                return redirect("changePassword")
            else:
                user.set_password(newPassword)
                user.save()
                messages.success(request, "Your password has been changed successfully")
                return redirect("home")  
    else:
        return render( request, "changePassword.html")



@login_required
def deleteAccount(request):
    user = request.user

    if request.method == "POST":
        password = request.POST["psw"]
        repassword = request.POST["re-psw"]

        if password != repassword:
            messages.error(request, "Passwords do not match")
            return redirect("deleteAccount")
        else:
            if user.check_password(password) == False:
                messages.error(request, "Password is incorrect")
                return redirect("deleteAccount")
            else:
                user.delete()
                messages.success(request, "Your account has been deleted successfully" )
                return redirect("signup")
    else:
         return render(request, "deleteAccount.html")






def resetPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email = email).first()

        if user is not None:
            randPassword = randint(11111111,99999999)
            user.set_password(randPassword)
            user.save()
            send_mail("Reset Password", f"Hi {user.username}! Your temporary password is {randPassword}. You can now log in and set a new password.", EMAIL_HOST_USER, [email]) 
            messages.success(request, "Your temporary password has been sent to your email. You can login and set a new password" )
            return redirect("login")
        else:
            messages.error(request, "There is no user with this email adress.")
            return redirect("resetPassword")
    else:
        return render(request, "resetPassword.html")



@login_required
def changeMail(request):
    
    user = request.user
    if request.method == "POST":
        password = request.POST["psw"]
        mail = request.POST["mail"]
        
        if user.check_password(password) == False:
                messages.error(request, "Password is incorrect")
                return redirect("changeMail")
        else:
            User.objects.filter(user=request.user).update(email = mail)
            messages.success(request, "Your email adress has been changed successfully")
            return redirect("home")
    
    return render(request, "changeMail.html")
