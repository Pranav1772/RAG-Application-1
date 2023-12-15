import json
from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from channels.generic.websocket import WebsocketConsumer
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'You are now connected!'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('message:',message)

        # Check if conversation chain exists
        if not hasattr(self, 'qa'):
            # Initialize conversation chain on first message
            pdf_details = get_object_or_404(PDF_Details, pdf_id=6)
            vectordb_path = pdf_details.pdf_vectordb_path
            embedding = OpenAIEmbeddings(openai_api_key='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')
            vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embedding)
            llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.6,openai_api_key='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')
            memory = ConversationBufferMemory(memory_key="chat_history",return_messages = True)
            retriever = vectordb.as_retriever()
            self.qa = ConversationalRetrievalChain.from_llm(llm,retriever = retriever,memory = memory)

        # Generate and send next utterance
        result = self.qa({"question":(message)})
        print("\nChatBot: "+result["answer"])
        # response = self.qa.next_utterance(message)

        self.send(text_data=json.dumps({
            'type':'chat',
            'question':message,
            'message':result["answer"]
        }))