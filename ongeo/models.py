from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Create your models here.


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=60)
    location= models.PointField()
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
    organisation = models.CharField(max_length=60, blank=True,null=True)
    location= models.PointField(null=True)
   


    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete

class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    organisation = models.ForeignKey(Organisation, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/blog/', blank = True, null =True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


    def __str__(self):
        return self.title


    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()


class UserCoords(models.Model):
    coords_long = models.IntegerField()
    coords_latt = models.IntegerField()
    organisation = models.ForeignKey(Organisation, related_name='usercoords', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
    


    def __str__(self):
        return f'{self. coords_long} {self.coords_latt}'


    def save_usercoords(self):
        self.save()

    def delete_usercoords(self):
        self.delete()


class Attendance(models.Model):
    organisation = models.ForeignKey(Organisation, related_name='inattendance', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def save_attendance(self):
        self.save()

    def delete_attendance(self):
        self.delete()