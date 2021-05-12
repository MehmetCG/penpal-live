from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.forms import ModelForm
from datetime import datetime




class UserProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=6, default="")
    country = models.CharField(max_length=40, default="")
    nativeLanguage = models.CharField(max_length=40, default="")
    practisingLanguage = models.CharField(max_length=40, default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to="images", default="default-profile-picture.jpg")
    is_online = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} Profile"



@receiver(pre_delete, sender=UserProfile)
def delete_image(sender, instance, **kwargs):
    if instance.image != "default-profile-picture.jpg":
        instance.image.delete()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



class Message(models.Model):
    objects = models.Manager()
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name= "sender", null=True)
    recipient = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "recipient", null=True)
    messageText = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add= True)
    

    def __str__(self):
        return (self.messageText)




class LatestSearch(models.Model):
    objects = models.Manager()
    searcher = models.OneToOneField(User, on_delete=models.CASCADE)
    minAge = models.IntegerField(default=0)
    maxAge = models.IntegerField(default=100)
    gender = models.CharField(max_length=6, default="Both")
    country = models.CharField(max_length=40, default="All")
    nativeLanguage = models.CharField(max_length=40, default="All")
    practisingLanguage = models.CharField(max_length=40, default="All")

    def __str__(self):
        return f"{self.searcher} Search"

@receiver(post_save, sender=User)
def create_search(sender, instance, created, **kwargs):
    if created:
        LatestSearch.objects.create(searcher=instance)




class LatestMessage(models.Model):
    objects = models.Manager()
    senders = models.ManyToManyField(User)    
    messageText = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return (self.messageText)


@receiver(pre_delete, sender=User)
def delete_image(sender, instance, **kwargs):
    instance.latestmessage_set.all().delete()



class UnreadMessage(models.Model):
    objects = models.Manager()
    sender2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name= "sender2", null=True)
    recipient2 = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "recipient2", null=True)