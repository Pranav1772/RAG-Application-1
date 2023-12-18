from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from django.http import HttpResponse, HttpResponseRedirect
import os, json
from django.urls import reverse
from django.core.cache import cache

# Create your views here.
def chat(request):
    pdf_details_list = PDF_Details.objects.all()
    pdf_data = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_data': pdf_data}
    return render(request,'ChatBot/chat.html',context)

def view_pdf(request,pdf_id):
    cache.set('my_pdf_data', pdf_id, timeout=300) 
    pdf_details = PDF_Details.objects.get(pk=pdf_id)
    return render(request, 'ChatBot/chat', {'pdf_details': pdf_details})
    # return HttpResponseRedirect(reverse('chatbot'))    

# def detail_pdf(request, pdf_id):
    
#     return render(request, 'pdf_detail.html', {'pdf_details': pdf_details})