from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from.models import Profile, Organisation,Post, UserCoords,Attendance

# Register your models here.
@admin.register(Organisation)
class OrganisationAdmin(OSMGeoAdmin):
    list_display = ('organisation_name', 'location')


@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    list_display = ('user', 'location')

@admin.register(Post)
class PostAdmin(OSMGeoAdmin):
    list_display = ('title', 'content')

  
@admin.register(UserCoords)
class UserCoordsAdmin(OSMGeoAdmin):
    # list_display = (' coords_long',' coords_long')
    pass

  
@admin.register(Attendance)
class AttendanceAdmin(OSMGeoAdmin):
    pass