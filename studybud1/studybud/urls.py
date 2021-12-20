
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#this is or was in the future i set a http request and appropriate response 
  #here it returns a httpresponse to our roomurl
#moved the code lied here to base app views.py and apps.py
#inorder to avoid the redundancy and complexity and crossfiring that occur by writing repeated request and response that may occur 
urlpatterns = [  #this  is a list
    path('admin/', admin.site.urls),
    #'blah blah' setsup the route ie our web url 
    path('',include('base.urls')),
    path('api/',include('base.api.urls')),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#as we are menttioning the paths we have to import the path to our urls file ie  line 3