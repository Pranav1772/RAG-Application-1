import json
from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from channels.generic.websocket import WebsocketConsumer
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from django.contrib.messages import get_messages

class ChatConsumer(WebsocketConsumer):
    def connect(self):      
        self.accept()             

    def my_consumer_type(self, event):
        # Handle the received data
        data = json.loads(event['text'])
        message = data['message']

        # Do something with the received data
        # ...

        # Send a response back to the client
        self.send(text_data=json.dumps({
            'message': 'Data processed successfully'
        }))  

    def receive(self, text_data,**kwargs):                 
        #  message_type = data.get('type')
        data = json.loads(text_data)
        if message_type == 'send_data':
            self.send(text_data=json.dumps({'message': 'Data received successfully'}))
            
            
        # Check if conversation chain exists
        if not hasattr(self, 'qa'):            
            # Initialize conversation chain on first message
            pdf_details = get_object_or_404(PDF_Details, pdf_id=self.pdf_id)
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

        def createPersona(self, ch):
            gen_prompt = '''
                            You are a general assistant AI chatbot here to assist the user based on the PDFs they uploaded,
                            and the subsequent openAI embeddings. Please assist the user to the best of your knowledge based on 
                            uploads, embeddings and the following user input. USER INPUT: 
                        '''

            acc_prompt = '''
                            You are a academic assistant AI chatbot here to assist the user based on the academic PDFs they uploaded,
                            and the subsequent openAI embeddings. This academic persona allows you to use as much outside academic responses as you can.
                            But remember this is an app for academix PDF question. Please respond in as academic a way as possible, with an academix audience in mind
                            Please assist the user to the best of your knowledge, with this academic persona
                            based on uploads, embeddings and the following user input. USER INPUT: 
                        '''

            witty_prompt = '''
                            You are a witty assistant AI chatbot here to assist the user based on the PDFs they uploaded,
                            and the subsequent openAI embeddings. This witty persona should make you come off as lighthearted,
                            be joking responses and original, with the original user question still being answered.
                            Please assist the user to the best of your knowledge, with this comedic persona
                            based on uploads, embeddings and the following user input. USER INPUT: 
                        '''
            if ch==1: prompt = gen_prompt
            elif ch==2: prompt = acc_prompt
            elif ch==3: prompt = witty_prompt
            return prompt