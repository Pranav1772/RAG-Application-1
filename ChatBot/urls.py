from django.urls import path, include
from ChatBot import views

urlpatterns = [
    path("chat/",views.chat,name='chatbot'),
]
