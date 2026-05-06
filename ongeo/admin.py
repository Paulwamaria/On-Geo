from django.contrib import admin
from django import forms
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.geos import Point
from .models import Profile, Organisation, Post, Attendance, AllLogin, AllAtendees, CheckPoint

# Register your models here.
@admin.register(Organisation)
class OrganisationAdmin(OSMGeoAdmin):
    fields = ('organisation_name', 'description', 'location', 'logo', 'members')
    list_display = ('organisation_name', 'short_description', 'location')
    search_fields = ('organisation_name', 'description')

    @admin.display(description='Description')
    def short_description(self, obj):
        if len(obj.description) > 80:
            return f'{obj.description[:77]}...'
        return obj.description

    class Media:
        js = ('js/admin_current_location.js',)


@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    list_display = ('user','profile_pic','bio')

@admin.register(Post)
class PostAdmin(OSMGeoAdmin):
    list_display = ('title', 'content')


class CheckPointAdminForm(forms.ModelForm):
    latitude = forms.FloatField(
        required=False,
        help_text='Optional. Enter decimal latitude, for example -1.3034532.',
    )
    longitude = forms.FloatField(
        required=False,
        help_text='Optional. Enter decimal longitude, for example 36.7927116.',
    )

    class Meta:
        model = CheckPoint
        fields = ('name', 'organisation', 'latitude', 'longitude', 'point', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['point'].required = False

        if self.instance and self.instance.point:
            self.fields['latitude'].initial = self.instance.point.y
            self.fields['longitude'].initial = self.instance.point.x

    def clean(self):
        cleaned_data = super().clean()
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        point = cleaned_data.get('point')

        if latitude is None and longitude is None:
            if not point:
                raise forms.ValidationError('Select a point on the map or enter latitude and longitude.')
            return cleaned_data

        if latitude is None or longitude is None:
            raise forms.ValidationError('Enter both latitude and longitude.')

        if not -90 <= latitude <= 90:
            self.add_error('latitude', 'Latitude must be between -90 and 90.')

        if not -180 <= longitude <= 180:
            self.add_error('longitude', 'Longitude must be between -180 and 180.')

        if self.errors:
            return cleaned_data

        cleaned_data['point'] = Point(longitude, latitude, srid=4326)
        return cleaned_data


@admin.register(CheckPoint)
class CheckPointAdmin(OSMGeoAdmin):
    form = CheckPointAdminForm
    fields = ('name', 'organisation', 'latitude', 'longitude', 'point', 'is_active')
    list_display = ('name', 'organisation', 'point', 'is_active')
    list_filter = ('organisation', 'is_active')
    search_fields = ('name', 'organisation__organisation_name')

    class Media:
        js = ('js/admin_current_location.js',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_active:
            CheckPoint.objects.filter(
                organisation=obj.organisation,
                is_active=True,
            ).exclude(pk=obj.pk).update(is_active=False)

  
@admin.register(Attendance)
class AttendanceAdmin(OSMGeoAdmin):
    pass

@admin.register(AllLogin)
class AllLoginAdmin(OSMGeoAdmin):
    pass


@admin.register(AllAtendees)
class AllAtendeesAdmin(OSMGeoAdmin):
   list_display = ('user', 'first_name','last_name')
