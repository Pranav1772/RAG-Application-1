from django.shortcuts import render, get_object_or_404
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
    pdf_count = PDF_Details.objects.all().count()
    context = {'username_count': username_count,'pdf_count':pdf_count}
    return render(request,'Profiles/dashboard.html',context)

def manage_users(request):
    user_details_list = UserDetail.objects.all()
    user_details = [{'user_id': user.user_id, 'user_name': user.user_name,'user_email':user.user_email} for user in user_details_list]
    context = {'user_details': user_details}
    return render(request,'Profiles/manage_users.html',context)

def manage_docs(request):
    pdf_details_list = PDF_Details.objects.all()
    pdf_details = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_details': pdf_details}
    return render(request,'Profiles/manage_docs.html',context)

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
     
def update_user(request,user_id):
    user = get_object_or_404(UserDetail, user_id=user_id)
    return render(request,'Profiles/update_users_page.html',{'user': user})

# def update_users_page(request):  
#     if request.method == 'POST':        
#         user_id = request.POST.get('user_id')
#         print(request.POST.get('user_id'))
#         user = get_object_or_404(UserDetail, user_id=user_id)
#         user.user_name = request.POST.get('user_name')
#         user.user_email = request.POST.get('user_email')
#         user.user_password = request.POST.get('user_password')    
#         user.save()

def update_activity(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        print(user_id)        
        user = get_object_or_404(UserDetail, user_id=user_id)
        user.user_name = request.POST.get('user_name')
        user.user_email = request.POST.get('user_email')
        user.user_password = request.POST.get('user_pass')
        user.save()
    return HttpResponseRedirect(reverse('manage_users'))

def delete_user(request,user_id):
    user = get_object_or_404(UserDetail, user_id=user_id)
    print(user)
    if request.method == 'POST':
        user.delete()
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
        embedding = OpenAIEmbeddings(openai_api_key='') #Remember to use your api key 
        vectordb = Chroma.from_documents(documents=docs, embedding=embedding, persist_directory=vectordb_path)        
        return HttpResponseRedirect(reverse('manage_docs'))

def delete_pdf(request,pdf_id):
    pdf = get_object_or_404(PDF_Details, pdf_id=pdf_id)
    if request.method == 'POST':
        pdf.delete()
    return HttpResponseRedirect(reverse('manage_docs'))
