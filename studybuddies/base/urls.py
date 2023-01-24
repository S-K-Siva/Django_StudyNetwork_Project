from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('',views.home, name = "home-view"),
    path('details/<str:pk>/',views.details,name="detail-view"),
    path('create-room/',views.create_room,name="create-room"),
    path('update-room/<str:pk>',views.update_room,name="update-room"),
    path('delete-room/<str:pk>',views.delete_room,name="delete-room"),
    path('login/',views.login_register,name='login-page'),
    path('logout/',views.logout_process,name='logout-page'),
    path('register/',views.register_user,name='register-page'),
    path('delete_message/<str:pk>/',views.del_message,name='del_message'),
    path('profile/<str:pk>/',views.profile_view,name='profile-view'),
    path('edit-profile/',views.Update_user,name='edit-profile'),
    path('topics/',views.all_topic,name='topic'),
    path('apis/',include("base.api.urls")),
    path('settings/',views.Update_user,name = "setting"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)