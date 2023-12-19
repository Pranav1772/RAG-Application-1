import json
from django.shortcuts import render, get_object_or_404
from Profiles.models import PDF_Details
from channels.generic.websocket import WebsocketConsumer
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from django.core.cache import cache
import google.generativeai as genai

class ChatConsumer(WebsocketConsumer):
    def connect(self):      
        self.accept()           

    def receive(self, text_data):      
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        pdf_id = cache.get('my_pdf_data')
        print(pdf_id)

        GOOGLE_API_KEY=('AIzaSyCheg7DR_6qoTYlcAWThlJukPn-NeCyMO0')
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro-vision')            
        response = model.generate_content(["Describe what is present in the image in details.", img], stream=True)
        response.resolve()

        # Check if conversation chain exists
        if not hasattr(self, 'qa'):           
            # Initialize conversation chain on first message
            pdf_details = get_object_or_404(PDF_Details, pdf_id=pdf_id)
            vectordb_path = pdf_details.pdf_vectordb_path
            embedding = OpenAIEmbeddings(openai_api_key='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')
            vectordb = Chroma(persist_directory=vectordb_path, embedding_function=embedding)
            llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.6,openai_api_key='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')
            memory = ConversationBufferMemory(memory_key="chat_history",return_messages = True)
            retriever = vectordb.as_retriever()
            self.qa = ConversationalRetrievalChain.from_llm(llm,retriever = retriever,memory = memory)

        # Generate and send next utterance
        prompt = """You are a general assistant AI chatbot here to assist the user based on the PDFs they uploaded,
                    and the subsequent openAI embeddings. Please assist the user to the best of your knowledge based on 
                    uploads, embeddings and the following user input. And give the output in HTML renderable format (for
                    example if there is end of line then replace it with br tag and when asked for table then arrange the table tag
                    and tr and td tags) USER INPUT:"""
        question = prompt + message
        result = self.qa({"question":(question)})
        print("\nChatBot: "+result["answer"])
        # response = self.qa.next_utterance(message)

        self.send(text_data=json.dumps({
            'type':'chat',
            'question':message,
            'message':result["answer"],
        }))

        # def image_processing(self):
        #     GOOGLE_API_KEY=('AIzaSyCheg7DR_6qoTYlcAWThlJukPn-NeCyMO0')
        #     genai.configure(api_key=GOOGLE_API_KEY)
        #     model = genai.GenerativeModel('gemini-pro-vision')

        #     response = model.generate_content(["Describe what is present in the image in details.", img], stream=True)
        #     response.resolve()
        #     print(response.text)

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