from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static  import static
from .views import PostCreateView,NotificationCreateView,PostUpdateView,PostDeleteView
from . import views



urlpatterns=[
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('setup/',views.no_setup,name='setup'),
    path('posts/',views.post,name='posts'),
    path('logins/',views.attend,name='logins'),
    path('attends/',views.attendees_list,name='attends'),
    path('register/',views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profile/logout.html'), name='logout'),
    path('profile/',views.profile, name = 'profile'),
    path('attendance/',views.attendance, name = 'attendance'),
    path('save_to_db/',views.save_to_db, name = 'save-to-db'),
    path('distance/',views.get_distance, name = 'get-distance'),
    path('profile/details/<str:username>/',views.display_profile, name = 'profile-detail'),
    path('post/new/',PostCreateView.as_view(), name = 'post-create'),
    path('notification/new/',NotificationCreateView.as_view(), name = 'notification-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(), name = 'post-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)