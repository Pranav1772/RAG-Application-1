from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.urls import reverse

# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory

# Create your views here.
def chat(request):
    pdf_details_list = PDF_Details.objects.all()
    pdf_data = [{'pdf_id': pdf.pdf_id, 'pdf_name': pdf.pdf_name} for pdf in pdf_details_list]
    context = {'pdf_data': pdf_data}
    return render(request,'ChatBot/chat.html',context)

def view_pdf(request,pdf_id):
    # print(type(pdf_id))
    # pdf_details = get_object_or_404(PDF_Details, pdf_id=pdf_id)
    # print(pdf_details)
    # vectordb_path = pdf_details.pdf_vectordb_path
    # embedding = OpenAIEmbeddings(openai_api_key='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')
    # vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embedding)
    # llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.6,openai_api_key='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')
    # memory = ConversationBufferMemory(memory_key = "chat_history",return_messages = True)
    # retriever = vectordb.as_retriever()
    # qa = ConversationalRetrievalChain.from_llm(llm,retriever = retriever,memory = memory)
    
    return HttpResponseRedirect(reverse('chatbot'))

    # if os.path.exists(pdf_path):
    #     with open(pdf_path, 'rb') as pdf_file:
    #         response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    #         print(response)
    #         response['Content-Disposition'] = f'inline; filename="{pdf_details.pdf_name}"'
    #         return response
    # else:
    #     return HttpResponse('PDF not found', status=404)