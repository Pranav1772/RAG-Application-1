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
    username_count = UserDetail.objects.all().count()
    context = {'username_count': username_count,}
    return render(request,'Profiles/dashboard.html',context)

def manage_users(request):
    return render(request,'Profiles/manage_users.html')

def manage_docs(request):
    return render(request,'Profiles/manage_docs.html')

from django.shortcuts import render, redirect

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_email = request.POST.get('useremail')
        user_password = request.POST.get('userpass')
        new_user = UserDetail(
            user_name=username,
            user_email=user_email,
            user_password=user_password,
        )
        new_user.save()
        return HttpResponseRedirect(reverse('manage_users'))        

def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        vectordb_path = os.path.join(settings.MEDIA_ROOT, 'vectordb', pdf_file.name)
        pdf_details = PDF_Details(pdf_name=pdf_file.name,pdf_vectordb_path=vectordb_path)        
        pdf_details.pdf_file.save(pdf_file.name,pdf_file)        
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', pdf_file.name)
        loader = PyPDFLoader(pdf_file_path)
        pages = loader.load()
        text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=150, length_function=len)
        docs = text_splitter.split_documents(pages)
        embedding = OpenAIEmbeddings(openai_api_key='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')
        vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=vectordb_path)        
        return HttpResponseRedirect(reverse('manage_docs'))
