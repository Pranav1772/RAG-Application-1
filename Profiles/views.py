from django.shortcuts import render
from .models import UserDetail, PDF_Details
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.conf import settings
import os

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter


# Create your views here.
def dashboard(request):
    return render(request,'Profiles/dashboard.html')

def manage_users(request):
    return render(request,'Profiles/manage_users.html')

def manage_docs(request):
    return render(request,'Profiles/manage_docs.html')

from django.shortcuts import render, redirect

def add_user(request):
    if request.method == 'POST':
        # Get the submitted data
        username = request.POST.get('username')
        user_email = request.POST.get('useremail')
        user_password = request.POST.get('userpass')

        # Create a new UserDetail object
        new_user = UserDetail(
            user_name=username,
            user_email=user_email,
            user_password=user_password,
        )

        # Validate the data (optional)

        # Save the object
        new_user.save()

        # Redirect or display success message
        return HttpResponseRedirect(reverse('manage_users'))

    else:
        # Render the form for GET requests
        return render(request, 'Profiles/manage_users.html')
    

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_details = PDF_Details(pdf_name=pdf_file.name)
        pdf_details.pdf_file.save(pdf_file.name,pdf_file)
        vectordb_file_path = os.path.join(settings.MEDIA_ROOT, 'vectordb', pdf_file.name)
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', pdf_file.name)
        loader = PyPDFLoader(pdf_file_path)
        pages = loader.load()
        print(len(pages))
        # pdf_details = PDF_Details(pdf_name=pdf_file.name)
        # pdf_details.pdf_file.save(pdf_file.name,pdf_file)
        pdf_file_path = pdf_details.pdf_file.path

        print(pdf_file_path)
