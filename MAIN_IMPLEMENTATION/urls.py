from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.signin,name='signing'),
    path('profiles/', include('Profiles.urls')),
    path('chatbot/', include('ChatBot.urls')),
    
]
