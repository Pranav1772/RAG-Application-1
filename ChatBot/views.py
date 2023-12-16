from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from django.http import HttpResponse, HttpResponseRedirect
import os, json
from django.urls import reverse
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# Create your views here.
def chat(request):
    pdf_details_list = PDF_Details.objects.all()
    pdf_data = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_data': pdf_data}
    return render(request,'ChatBot/chat.html',context)

def view_pdf(request,pdf_id):       
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send(
        'india',
        {
            'type':'chat.message',
            'message':pdf_id
        }
    ))
    return HttpResponseRedirect(reverse('chatbot'))

    # if os.path.exists(pdf_path):
    #     with open(pdf_path, 'rb') as pdf_file:
    #         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    #         print(response)
    #         response['Content-Disposition'] = f'inline; filename="{pdf_details.pdf_name}"'
    #         return response
    # else:
    #     return HttpResponse('PDF not found', status=404)