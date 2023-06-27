from django.shortcuts import render 
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import logout
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *
from django.db.models import Q
from base.form import CreateRoomForm
# rooms = [ 
#          {'id': 1 ,'title':'Lets learn Python'},
#          {'id': 2 ,'title':'Lets learn PHP'},
#          {'id': 3 ,'title':'Lets learn NODE JS'},
#          {'id': 4 ,'title':'Lets learn RUBY'},
# ]



def home(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)) 

    #rooms will give the query set
    get_message=Message.objects.filter(Q(room__topic__name__icontains=q))
    #print(get_message)
    topic=Topic.objects.all()
    #print(topic)
    room_count=rooms.count()
    context={'rooms':rooms,
             'topic':topic,
             'room_count':room_count,
             'get_message':get_message,}
    return render(request ,'base/home.html',context)

def room(request,pk):
    rooms=Room.objects.get(id=pk)
    #print("ROOMS IS : " , rooms)
    room_msg=rooms.message_set.all().order_by('-created_at')
    #print(room_msg)
    get_participants=rooms.participant.all()
    #print("PARTICIPANTS ARE :  " , get_participants)
    if request.method == 'POST':
       room_message=Message.objects.create(
          user=request.user,
          room=rooms,
          body=request.POST.get('body')
       )
       rooms.participant.add(request.user)
       return redirect('room',pk=rooms.id)

    context={'rooms':rooms,'room_messages':room_msg ,'get_participants':get_participants,}
    return render(request ,'base/room.html',context)

@login_required(login_url='User-login')
def CreateRoom(request):
    form=CreateRoomForm()
    if request.method == "POST":
          #print(request.POST)
          form=CreateRoomForm(request.POST)
          if form.is_valid():
           room=form.save(commit=False)
           room.host=request.user
           room.save()
           return redirect("/")
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='User-login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=CreateRoomForm(instance=room)
    if request.method == "POST":
     form=CreateRoomForm(request.POST,instance=room)
     if form.is_valid():
        form.save()
        return redirect("/")
    context={'form':form}
    return render(request,"base/room_form.html",context)

@login_required(login_url='User-login')
def DeleteRoom(request,pk):
   room=Room.objects.get(id=pk)
   #NEEDS TO BE ADDED MORE FUNCTIONALITY
   room.delete()
   return redirect('/')
      

def loginpage(request):
   
   if request.user.is_authenticated:
      return redirect('home')
   
   if request.method=="POST":
      username=request.POST.get('username')
      password=request.POST.get('password')

      try:
        user=User.objects.get(username=username)
      except:
          messages.error(request, "User Does Not Exists")
          
      user = authenticate(request,username=username, password=password)

      if user is not None:
         login(request,user)
         return redirect("/")
      else:
         messages.error(request, "Username Or Password Does Not Match")
   context={}
   return render(request,"base/login.html",context)


def UserLogOut(request):
   logout(request)
   return redirect('/')

def RegisterUser(request):
   form=UserCreationForm()
   #print(form)
   if request.method=='POST':
      form=UserCreationForm(request.POST)
      if form.is_valid():
         user=form.save()
         user.save()
         #user=authenticate(request, username=user.username ,password=user.password)
         login(request,user)
         return redirect('home')
      else:
         messages.error(request, "An Error Occured During Registration")

   return render(request,"base/register.html",{'form':form})

# def deletemessage(request,pk):
#    message=Message.object.get(id=pk)
#    message.delete()
#    return redirect('/')

def UserProfile(request,pk):
   q = request.GET.get('q') if request.GET.get('q') !=None else ''
   user=User.objects.get(id=pk)
   get_message=Message.objects.filter(Q(room__topic__name__icontains=q))
   context={
      'user':user,
      'get_message':get_message,
   }
   return render(request,"base/profile.html",context)
