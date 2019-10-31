from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Organisation, UserCoords, Attendance




class OnGeoRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=60,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(required = True,label='',widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Email'}))
    first_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    
    password1 = forms.CharField(max_length = 30,required = True, label='', widget = forms.TextInput(attrs={
        "class":"form-control",
        "name":"password1",
        "type":"password",
        "placeholder":"Password"
    }))
    password2 = forms.CharField(max_length = 30,required = True,label='', widget = forms.TextInput(attrs={
        "class":"form-control",
        "name":"password2",
        "type":"password",
        "placeholder":"Repeat Password"
    }))

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','username','password1','password2']



    def save(self, commit=True):
        user =super(OnGeoRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.last_name = self.cleaned_data['first_name']
        user.first_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()


        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required = True,label='',widget=forms.TextInput(attrs = {'class':'form-control','placeholder':'Email'}))
    first_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    username = forms.CharField(max_length=60,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio', 'location']



class UserCoordinateForm(forms.ModelForm):
    class Meta:
        model = UserCoords
        fields = ['coords_long','coords_latt']




class UserAttendanceForm(forms.ModelForm):
    first_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name','id':'fname'}))
    last_name = forms.CharField(max_length=256,required = True, label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name','id':'lname'}))
    class Meta:
        model = Attendance
        fields = ['first_name','last_name']



