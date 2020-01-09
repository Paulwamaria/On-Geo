from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,DeleteView
from geopy.distance import distance as geopy_distance
from datetime import date
from .forms import OnGeoRegistrationForm,UserUpdateForm,ProfileUpdateForm, UserAttendanceForm, SwitchCommunityForm
from .models import Profile, Organisation, Post,Attendance,Notification, AllLogin, AllAtendees,CheckPoint
from .tables import AttendeesTable

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
        org = request.user.profile.community
        distance = request.GET.get('distance')
        print("****************",org)
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
     
        initial_count= AllAtendees.objects.all().count()
       
        # attendant = Attendance.objects.filter(first_name=first_name, last_name=last_name).first()
        # if attendant == None:
        #     attendant = Attendance(first_name=first_name, last_name=last_name)
        #     attendant.organisation = org
        #     attendant.save()


        attendee = AllAtendees.objects.filter(user = request.user,checked_in_on__date = date.today())
        print("nananana", attendee.count())
        if attendee.count() == 0:
            AllAtendees.objects.create(user=request.user, first_name=first_name, last_name =last_name)
    

        attendees =AllAtendees.objects.all().count()
        attendants = Attendance.objects.all().count()
        # todays_attendants = Attendance.objects.filter(created_on__date=date.today()).count()
        # print (todays_attendants)
        if initial_count < attendees:
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
        fixed_position = (-1.3034531999999999, 36.7927116)
        #fixed_position = (-1.2828671999999999, 36.831232)


        distance = geopy_distance(user_position, fixed_position)
        
        my_user ={
            "first_name":user.first_name,
            "last_name":user.last_name
        } 
        dist = distance.meters
        context = {
            "distance":dist,
            "user":serialized_user,
            "user_data":my_user
        }
        print(dist)
      

        return JsonResponse(context,safe=False)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)    
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            profile = p_form.save()
            profile.profile_pic = p_form.cleaned_data['profile_pic']
            profile.save()
        return redirect("home")
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
        form.instance.organisation = Organisation.objects.get(organisation_name = self.request.user.profile.community)
        return super().form_valid(form)


class PointCreateView(LoginRequiredMixin,CreateView):
     
    model = CheckPoint
    success_url = ('/')
    fields = ['point','name']

    def form_valid(self,form):
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin,CreateView):
     
    model = Post
    success_url = ('/')
    fields = ['title','image','content','links']

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.organisation = Organisation.objects.get(organisation_name = self.request.user.profile.community)
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
    posts = Post.objects.filter(organisation__organisation_name=profile.community)
    notifications = Notification.objects.filter(organisation__organisation_name=profile.community)

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    
    

    context={
        "posts":posts,
        "notifications":notifications,
      
    }

    return render(request,'ongeo/posts.html',context)



def attend(request):
    attendee = AllAtendees.objects.filter(user = request.user,checked_in_on=date.today())
    if attendee == None:
        AllAtendees.objects.create(user=request.user, f_name=request.user.first_name, l_name = request.user.last_name, last_seen = request.user.last_login)
    attendees = AllAtendees.objects.filter(checked_in_on=date.today())
    first_atendee=AllAtendees.objects.last()

 
  


 
    return render(request,'profile/attendance.html')


def attendees_list(request):
    # attendee = AllAtendees.objects.filter(user = request.user,checked_in_on__date = date.today())
    # print("nananana", attendee.count())
    # if attendee.count() == 0:
    #     AllAtendees.objects.create(user=request.user, first_name=request.user.first_name, last_name = request.user.last_name)
  
    queryset = AllAtendees.objects.filter(checked_in_on__date=date.today())
    table = AttendeesTable(queryset)
    context = {
        "queryset": queryset,
        "table":table
    }
    return render(request, 'ongeo/attend_list.html', context)




def switch_community(request):
    if request.method == 'POST':
        community = Organisation.objects.filter(organisation_name__icontains =request.POST.get('community').lower()).first()
        if community == None:
            new_community = Organisation(organisation_name = request.POST.get('community') )
            new_community.save()
            community = new_community
        profile = request.user.profile
        profile.community =  community
        profile.save()

        return redirect()
        # c_form = SwitchCommunityForm(request.POST)
        # if c_form.is_valid():
           
            # c_form.save()
         
    # else:
    c_form = SwitchCommunityForm(instance = request.user.profile)
        
      


    context={
        'c_form':c_form,
      
    }
    return render(request, 'ongeo/switch_community.html',context)
