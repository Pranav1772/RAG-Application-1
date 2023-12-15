from django.urls import path, include
from ChatBot import views

urlpatterns = [
    path("chat/",views.chat,name='chatbot'),
    path('view-pdf/<int:pdf_id>/', views.view_pdf, name='view_pdf'),  # Corrected argument name to pdf_id
]
