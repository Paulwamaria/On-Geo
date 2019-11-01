from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,DeleteView
from geopy.distance import distance as geopy_distance
from .forms import OnGeoRegistrationForm,UserUpdateForm,ProfileUpdateForm, UserAttendanceForm
from .models import Profile, Organisation, Post,Attendance,Notification

def index(request):
    message = "Welcome to On-Geo Manager"


    context = {
        "message":message
    }
    return render(request,"ongeo/index.html", context)


def about(request):
    return render(request,'ongeo/about.html')



def no_setup(request):
    return render(request,'ongeo/no-setup.html')




def register(request):
    if request.method == 'POST':
        form = OnGeoRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            messages.success(request, f'Account created for {username}')
            return redirect('profile')
    else:
        form = OnGeoRegistrationForm()
    return render(request, 'profile/register.html', {'form': form})


@login_required
def attendance(request):
    if request.method == 'POST':
        attnd_form = UserAttendanceForm(request.POST)
        
            
        if attnd_form.is_valid():
            attnd_form.save()
            first_name = attnd_form.cleaned_data['first_name']
            last_name = attnd_form.cleaned_data['last_name']

            # my_attendant ={
            #     "first_name":first_name,
            #     "last_name":last_name,
            # }

            context={
            'attnd_form':attnd_form,
            # "attendant":my_attendant,
        
        }
        return render(request, 'profile/attendance.html',context)

            
    else:
        attnd_form = UserAttendanceForm()
         
    


    context={
        'attnd_form':attnd_form,
    
    }
    return render(request, 'profile/attendance.html',context)


def display_profile(request,username):
    profile = Profile.objects.get(user__username= username)

    user_posts = Post.objects.filter(user =profile.user).order_by('created_on')

    context={
        "profile":profile,
        "user_posts":user_posts
    }
    return render(request,'profile/profile_detail.html',context)


def save_to_db(request):
    if request.method == "GET":
        org = request.user.profile.organisation
        print("****************",org)
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        initial_count= Attendance.objects.all().count()
        attendant = Attendance.objects.filter(first_name=first_name, last_name=last_name).first()
        if attendant == None:
            attendant = Attendance(first_name=first_name, last_name=last_name)
            attendant.organisation = org
            attendant.save()

        attendants = Attendance.objects.all().count()
        if initial_count < attendants:
            return JsonResponse({'saved':True})
        else:
            return JsonResponse({'saved':False})

@login_required
def get_distance(request):
    if request.method == "GET":
        user = request.user
        serialized_user = serializers.serialize('json', [ user ])
        user_latitude = request.GET.get('user_latitude')
        user_longitude = request.GET.get('user_longitude')

        user_position = (user_latitude, user_longitude)

        # fixed_position = (41.8781, 87.6298)
        #fixed_position = (-1.3034531999999999, 36.7927116)
        fixed_position = (-1.2836864000000001, 36.831232)


        dista = geopy_distance(user_position, fixed_position)
        distance = dista.meters
        my_user ={
            "first_name":user.first_name,
            "last_name":user.last_name
        } 
        context = {
            "distance":distance,
            "user":serialized_user,
            "user_data":my_user
        }
        print(distance)
      

        return JsonResponse(context,safe=False)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)    
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance = request.user)
        
        p_form = ProfileUpdateForm(instance = request.user.profile)


    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'profile/profile.html',context)


class NotificationCreateView(LoginRequiredMixin,CreateView):
     
    model = Notification
    success_url = ('/')
    fields = ['content']

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.organisation = Organisation.objects.get(organisation_name = self.request.user.profile.organisation)
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin,CreateView):
     
    model = Post
    success_url = ('/')
    fields = ['title','image','content','links']

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.organisation = Organisation.objects.get(organisation_name = self.request.user.profile.organisation)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
     
    model = Post
    success_url=('/')
    fields = ['title','image','content','links']


    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()

        if self.request.user == post.user:
            return True

        return False

    def get_redirect_url(self,pk, *args, **kwargs):
        obj = get_object_or_404(Post, pk = pk)
        url= obj.get_absolute_url()
      
      
        return url

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = ('/')
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.user:
            return True

        return False


@login_required
def post(request):
  
    profile=Profile.objects.get(user=request.user)
    posts = Post.objects.filter(organisation__organisation_name=profile.organisation)
    notifications = Notification.objects.filter(organisation__organisation_name=profile.organisation)
    
    

    context={
        "posts":posts,
        "notifications":notifications,
      
    }

    return render(request,'ongeo/posts.html',context)


