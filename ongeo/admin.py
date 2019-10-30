from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from.models import Profile, Organisation

# Register your models here.
@admin.register(Organisation)
class OrganisationAdmin(OSMGeoAdmin):
    list_display = ('organisation_name', 'location')


@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    list_display = ('user', 'location')