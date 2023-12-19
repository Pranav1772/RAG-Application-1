from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from django.http import HttpResponse, HttpResponseRedirect
import os, json
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.urls import reverse
from django.core.cache import cache
import google.generativeai as genai
from django.conf import settings

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def chat(request):
    pdf_details_list = PDF_Details.objects.all()
    pdf_data = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_data': pdf_data}
    return render(request,'ChatBot/chat.html',context)

def view_pdf(request,pdf_id):
    cache.set('my_pdf_data', pdf_id, timeout=300) 
    pdf_details = PDF_Details.objects.get(pk=pdf_id)    
    pdf_details_list = PDF_Details.objects.all()
    pdf_data = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_data': pdf_data}
    return render(request,'ChatBot/chat.html',context)
    # return HttpResponseRedirect(reverse('chatbot'))    

@csrf_exempt
def upload_img(request):     
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['imgFile']

        # Save the uploaded file temporarily
        temporary_file = TemporaryUploadedFile(uploaded_file.name, uploaded_file.content_type, uploaded_file.size, None, None)
        temporary_file.write(uploaded_file.read())
        temporary_file.seek(0)

        # Store the temporary file in a specific directory
        temporary_file_path = default_storage.save('temp_uploaded_images/{}'.format(uploaded_file.name), temporary_file)

        # Close the temporary file
        temporary_file.close()

        # Create the absolute file path by combining the media root and the relative path
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, temporary_file_path)
        print(temporary_file_path)
        import PIL.Image

        img = PIL.Image.open(absolute_file_path)
        img
        GOOGLE_API_KEY=('AIzaSyCheg7DR_6qoTYlcAWThlJukPn-NeCyMO0')
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro-vision')            
        response = model.generate_content(["Describe what is present in the image in details.", img], stream=True)
        response.resolve()
        print(response.text)
        # Close the temporary file
        temporary_file.close()

        # Now, `temporary_file_path` contains the path to the stored temporary file
        return HttpResponse(f'Temporary file stored at: {temporary_file_path}')
    else:
        return HttpResponse('No image uploaded.')
    # if request.method == 'POST':
    #     img_file = request.FILES.get('imgFile')
    #     GOOGLE_API_KEY=('AIzaSyCheg7DR_6qoTYlcAWThlJukPn-NeCyMO0')
    #     genai.configure(api_key=GOOGLE_API_KEY)
    #     model = genai.GenerativeModel('gemini-pro-vision')            
    #     response = model.generate_content(["Describe what is present in the image in details.", img], stream=True)
    #     response.resolve()
    # return HttpResponseRedirect(request,'ChatBot/chat.html',context)
# def detail_pdf(request, pdf_id):
    
#     return render(request, 'pdf_detail.html', {'pdf_details': pdf_details})