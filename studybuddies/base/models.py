from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=200,null = True)
    avatar = models.ImageField(default = "avatar.svg",null = True)
    email = models.EmailField(unique = True,null=False)
    bio = models.TextField(null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    


class Topic(models.Model): 
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL,null=True) #we set null to true(for database)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank = True) # null true means, the data can be blank. 
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now = True) #auto now takes snapshot, It changes every single time.
    created = models.DateTimeField(auto_now_add = True) #it takes only timestamp. It never change.
    class Meta:
        ordering=['-updated','-created']
    def __str__(self): #Thunderstring function, it should return string.
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#one-to-many / many-to-one relationship.
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #if room get deleted, all message of the room will be deleted. 
    #models.set_null -> only message will be deleted
    body = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.body[0:50]


    
