from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=60)
    location= models.PointField(-1.3034531999999999, 36.7927116)
    logo = models.ImageField(upload_to='media/', blank = True, null =True)
    members = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organisation_name


    def save_organisation(self):
        self.save()

    @classmethod
    def delete_organisation(cls,Organisation):
        cls.objects


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic =  models.ImageField(upload_to='media/profile_pics', default='media/default.jpg')
    bio = models.TextField()
    location= models.PointField()
   


    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete