#this is my sub directory inorder to avoid the code redundancy and for code longevity and dont be truculent
#only for specific app also root directiory has one
from django.urls import path
from . import views
urlpatterns = [
    path('logout/',views.logoutUser,name="logout"), 

    path('register/',views.registerPage,name="register"), 

    path('login/',views.loginPage,name="login"), 
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name="room"),#here we route it to room and calling room from views file of our app and indexing it with name
#here pk value is got from the views.py tag
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),
    path('update-user/',views.updateUser,name="update-user"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),


]
#<str:pk> is string as primarykey for dynamic url routing (for contents inside our each study material ie learning room contents