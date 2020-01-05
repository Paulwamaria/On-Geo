from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from.models import Profile, Organisation,Post,Attendance,AllLogin,AllAtendees,CheckPoint

# Register your models here.
@admin.register(Organisation)
class OrganisationAdmin(OSMGeoAdmin):
    list_display = ('organisation_name', 'location')


@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    list_display = ('user','profile_pic','bio')

@admin.register(Post)
class PostAdmin(OSMGeoAdmin):
    list_display = ('title', 'content')


@admin.register(CheckPoint)
class CheckPointAdmin(OSMGeoAdmin):
    list_display = ('point', 'name')

  
@admin.register(Attendance)
class AttendanceAdmin(OSMGeoAdmin):
    pass

@admin.register(AllLogin)
class AllLoginAdmin(OSMGeoAdmin):
    pass


@admin.register(AllAtendees)
class AllAtendeesAdmin(OSMGeoAdmin):
   list_display = ('user', 'first_name','last_name')
