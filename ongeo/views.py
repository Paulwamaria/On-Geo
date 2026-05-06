from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
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
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = OnGeoRegistrationForm()
    return render(request, 'profile/register.html', {'form': form})


@login_required
def attendance(request):
    if request.method == 'POST':
        attnd_form = UserAttendanceForm(request.POST)

            
        if attnd_form.is_valid():
            if request.user.profile.community is None:
                messages.error(request, "Select a community before recording attendance.")
                return redirect('switch-community')
            attendance_record = attnd_form.save(commit=False)
            attendance_record.organisation = request.user.profile.community
            attendance_record.save()
            messages.success(request, "Attendance recorded.")

            context={
            'attnd_form':attnd_form,

        }
        return render(request, 'profile/attendance.html',context)

            
    else:
        attnd_form = UserAttendanceForm()
         
    


    context={
        'attnd_form':attnd_form,
    
    }
    return render(request, 'profile/attendance.html',context)


@login_required
def display_profile(request,username):
    profile = Profile.objects.get(user__username= username)

    user_posts = Post.objects.filter(user =profile.user).order_by('created_on')

    context={
        "profile":profile,
        "user_posts":user_posts
    }
    return render(request,'profile/profile_detail.html',context)


@login_required
def save_to_db(request):
    if request.method == "GET":
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
     
        initial_count= AllAtendees.objects.all().count()
       
        # attendant = Attendance.objects.filter(first_name=first_name, last_name=last_name).first()
        # if attendant == None:
        #     attendant = Attendance(first_name=first_name, last_name=last_name)
        #     attendant.organisation = org
        #     attendant.save()


        attendee = AllAtendees.objects.filter(user = request.user,checked_in_on__date = date.today())
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

        if not user_latitude or not user_longitude:
            return JsonResponse({'error': 'Missing user coordinates'}, status=400)

        user_position = (user_latitude, user_longitude)
        print("User Position:", user_position)

        active_community = getattr(user.profile, 'community', None)
        checkpoint = None
        if active_community:
            checkpoint = CheckPoint.objects.filter(
                organisation=active_community,
                is_active=True,
            ).order_by('-id').first()
        if active_community and checkpoint is None:
            return JsonResponse(
                {
                    'error': (
                        f"No active checkpoint is linked to "
                        f"{active_community.organisation_name}."
                    ),
                },
                status=404,
            )

        if checkpoint is None:
            checkpoint = CheckPoint.objects.filter(
                organisation__isnull=True,
                is_active=True,
            ).order_by('-id').first()

        if checkpoint is None:
            return JsonResponse(
                {'error': "No active checkpoint is configured."},
                status=404,
            )

        fixed_position = (
            checkpoint.point.y,
            checkpoint.point.x,
        )

        print("Checkpoint Position:", fixed_position)


        distance = geopy_distance(user_position, fixed_position)
        print("Distance (meters):", distance.meters)
        
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
        return JsonResponse(context,safe=False)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance = request.user)
        
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)    
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save()
            messages.success(request, "Profile updated.")
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
        if self.request.user.profile.community is None:
            return redirect('switch-community')
        form.instance.organisation = self.request.user.profile.community
        return super().form_valid(form)


class PointCreateView(LoginRequiredMixin,CreateView):
     
    model = CheckPoint
    success_url = ('/')
    fields = ['point','name','is_active']

    def form_valid(self,form):
        if self.request.user.profile.community is None:
            messages.error(self.request, "Select a community before creating a checkpoint.")
            return redirect('switch-community')
        form.instance.organisation = self.request.user.profile.community
        response = super().form_valid(form)
        if self.object.is_active:
            CheckPoint.objects.filter(
                organisation=self.object.organisation,
                is_active=True,
            ).exclude(pk=self.object.pk).update(is_active=False)
        return response


class PostCreateView(LoginRequiredMixin,CreateView):
     
    model = Post
    success_url = ('/')
    fields = ['title','image','content','links']

    def form_valid(self,form):
        form.instance.user = self.request.user
        if self.request.user.profile.community is None:
            return redirect('switch-community')
        form.instance.organisation = self.request.user.profile.community
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
    if profile.community is None:
        messages.info(request, "Select a community before viewing posts.")
        return redirect('switch-community')

    posts = Post.objects.filter(organisation=profile.community)
    notifications = Notification.objects.filter(organisation=profile.community)

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



@login_required
def attend(request):
    AllAtendees.objects.get_or_create(
        user=request.user,
        checked_in_on__date=date.today(),
        defaults={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        },
    )
    return render(request,'profile/attendance.html')


@login_required
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




@login_required
def switch_community(request):
    if request.method == 'POST':
        community_name = request.POST.get('community')
        if not community_name:
            messages.error(request, "Select a community.")
            return redirect('switch-community')
        community = Organisation.objects.filter(organisation_name__iexact=community_name).first()
        if community is None:
            community = Organisation.objects.create(organisation_name=community_name)
        profile = request.user.profile
        profile.community = community
        profile.save()

        messages.success(request, f"Active community switched to {community.organisation_name}.")
        return redirect('posts')
         
    # else:
    c_form = SwitchCommunityForm(instance = request.user.profile)
        
      


    context={
        'c_form':c_form,
      
    }
    return render(request, 'ongeo/switch_community.html',context)
