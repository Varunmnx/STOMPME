from django.shortcuts import render,redirect
from base.models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
  #the django inbuld user registration form
 




def logoutUser(request):
    logout(request)
    return redirect('home')
     

def registerPage(request):
     
     form = MyUserCreationForm()

     if request.method =='POST':
         form = MyUserCreationForm(request.POST)
         if form.is_valid(): 
             user = form.save(commit=False)
             user.username = user.username.lower()
             user.save()
             login(request,user)
             return redirect('home')
         else:
             messages.error(request,'an error occured during registration !')    
   
     context =  {'form':form}
     return render(request,'base/login_register.html',context)



#note that we started room from here and we indexed it with rooms name in the dictionary
def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else '' #for gettinfg into the room that we selected from the filter panel

    rooms=Room.objects.filter(Q(topic__name__icontains=q) 
    |
    Q(name__icontains=q)
    |
    Q(description__icontains=q)) #if request.GET.get('q') != None else '' #this assigns the rooms variable with the one we  added from the admin panel here we can replace i with starts with and ends with 
    
    topics=Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #this returns the entire room messages along with the room message filtration

    context={'rooms': rooms,'topics':topics,'room_count':room_count, 'room_messages':room_messages } #assigned our dictionary data to context inorder to avoid code complexity
    return render(request,'base/home.html',context) #edited the httpResponse ,#rooms refered in form of dictionary  inorder to display  room data in our template

 

def room(request,pk):#here pk is what we are passing as a primary key which place holds the value of our dynamic url  mentioned in urls.py 
   room = Room.objects.get(id=pk)#this is for getting the dynamic url that is created when the rooms are created id is automatically generated
  
   room_messages=room.message_set.all().order_by('-created') #returns  messages related to a specific room iemessage in models.py and the newest will be first
  
   participants=room.participants.all()#calling related element from the many to many relationship 
  
   #for the commentbox and comment
   if request.method == 'POST':
       message = Message.objects.create(
           user=request.user,
           room = room,
           body = request.POST.get('body')
       )
       room.participants.add(request.user)
       return redirect('room',pk=room.id)
       
   context = {'room':room,'room_messages':room_messages,'participants':participants,}     #room here is a new variable   
   return render(request,'base/room.html',context)#edited the httpResponse passing dictionary assigned to a variable as a http response
    #11/23/21 now app templates are inside of our app folder and our main templates are inside of our root folder 


@login_required(login_url='login') #for making the user to login to create a room or even use the features of the website
def createRoom(request):
    form = RoomForm()
#saves the data to database and checks if data is valid and redirects to home page
    topics = Topic.objects.all()    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) #get or create method takes 2 variable in the initialisation section by which new topics created or old one gets updated in the model

        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )     
        return redirect('home')
    
    context = {'form': form,'topics':topics } #to sleeve using templates
    return render(request,'base/room_form.html',context)

#to update the room with new values
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed here ')


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST,instance=room) #replace the value stored in the room instance with the dic value returned by the page
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')   
    context={'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)

#this is to delete the room by the use of delete.html
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST': #this is a input request
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


def loginPage(request):
#to avoid the login of the user through the link and redirecting him

    page = 'login'


    if request.user.is_authenticated:
       return redirect('home')


    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password =request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'user doesnot exist')    

        user = authenticate(request,email=email,password=password)   
#user authentication method along with the redirection to home page if that user name donot exist
        if user is not None: #if user has something or nothing then 
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password doesnot exist')

    context={'page':page}
    return render(request,'base/login_register.html',context)

#this is user comment creation 

#messages can be deleted
@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('you are not allowed here !!')

    if request.method == 'POST':
        message.delete()    
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})    


def userProfile(request,pk):
    user= User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics= Topic.objects.all()
    context = {'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):   
    user = request.user
    form = UserForm(instance=user)
    
    if request.method =='POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context={'form':form}
    return render(request,'base/updateuser.html',context) 

    
def topicsPage(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else '' #for gettinfg into the room that we selected from the filter panel
    
    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html', {'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})    