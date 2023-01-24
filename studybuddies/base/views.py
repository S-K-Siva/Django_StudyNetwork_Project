from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm,UserRegisterForm,UserUpdateForm
from django.http import HttpResponse,HttpResponseRedirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages
# Create your views here.

# stats = [
#     {'Rank':2,'Company':'Samsung'},
#     {'Rank':1,'Company':'Apple'},
#     {'Rank':4,'Company':'Redmi'},
#     {'Rank':3,'Company':'OnePlus'},
# ]
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    data = Room.objects.filter(Q(topic__name__icontains=q) |
    Q(host__username__icontains=q))
    topics = Topic.objects.all()
    recent_post = Message.objects.all().order_by('-created')
    return render(request,'base/home.html',{'statistics':data,'topics':topics,'recent_post':recent_post})
@login_required(login_url='login-view')
def details(request,pk):
    key = pk
    Current = None
    data = Room.objects.get(id = pk)
    if request.method == "POST":
        messages = Message.objects.create(
            user = request.user,
            room = data,
            body = request.POST.get('body'),
        )
        messages.save()
        data.participants.add(request.user)
    all_messages = data.message_set.all().order_by('-created')
    participants = data.participants.all()
    print(participants)
    context = {'brand':data,'participants':participants,'all_messages':all_messages}

    return render(request,'base/details.html',context = context)
@login_required(login_url='login-view')
def del_message(request,pk):
    message_to_delete = Message.objects.get(id=pk)
    if request.method == "POST":
        temp = message_to_delete.room
        message_to_delete.delete()
        all_messages = temp.message_set.all()
        users = [x.user for x in all_messages]
        if request.user not in users:
            temp.participants.remove(request.user)
        return redirect('detail-view',message_to_delete.room.id)
    else:
        messages.error(request,'An error occurred while deleting the message!')
    return render(request,'base/del_message.html',context = {'message':message_to_delete})
@login_required(login_url='login-view')
def create_room(request):
    form = RoomForm()
    topic = Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            description = request.POST.get('description'),
            name = request.POST.get('name')
        )
        return redirect('home-view')
    return render(request,'base/room_form.html',context = {'form':form,'statistics':Topic.objects.all()})

@login_required(login_url='login-view')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home-view')
    return render(request,'base/room_form.html',context = {'form':form})

@login_required(login_url='login-view')
def delete_room(request,pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home-view')
    return render(request,'base/delete.html',context = {'object':room})


def profile_view(request,pk):

    user = User.objects.get(id=pk)
    all_topics = Topic.objects.all()
    rooms = user.room_set.all()
    all_messages = user.message_set.all().order_by('-created')    
    return render(request,'base/profile.html',context = {'user':user,'all_topics':all_topics,'all_messages':all_messages,'rooms':rooms})
@login_required(login_url='login-view')
def Update_user(request):
    user = request.user
    form = UserUpdateForm(instance = user)
    if request.method == "POST":
        form = UserUpdateForm(request.POST,request.FILES,instance = user)
        if form.is_valid:
            form.save()
            return redirect('profile-view',request.user.id)
    
    return render(request,'base/edit-user.html',{'form':form,'user':request.user})
def login_register(request):
    if request.user.is_authenticated:
        return redirect('home-view')
    if request.method ==  'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User doesn\'nt exist ')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            messages.success(request,'LoggedIn Successfully!')
            login(request,user)
            return redirect('home-view')
        else:
            messages.error(request, 'Username and Password Invalid')
    return render(request,'base/login_register.html',context = {})

def logout_process(request):
    logout(request)
    return redirect('login-page')

def register_user(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            login(request,user)
            return redirect('home-view')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/register.html',{'form':form})
def all_topic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    return render(request, 'base/topics.html',{'topics':topics})
# def register_user(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             age = form.cleaned_data.get('age')
#             gender = form.cleaned_data.get('gender')
#             profile_pic = form.cleaned_data.get('profile_pic')
#             bio = form.cleaned_data.get('bio')
#             email = form.cleaned_data.get('email')
#             user = User.objects.get(username=username)
#             user_data = Profile.objects.create(user=user, age=age, gender=gender,email=email,profile_pic=profile_pic,bio=bio)
#             user_data.save()
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'base/signupform.html', {'form':form})