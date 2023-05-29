# uvicorn main:app
# uvicorn main:app --reload

import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Body, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from pydantic import BaseModel
from openai_requests.openai_requests import get_chat_response
from langchain_requests.custom_chains import get_summary_chain
from langchain_requests.multiple_requests import chat_on_file
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma, FAISS
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
import PyPDF2
from io import BytesIO
from typing import Optional
import pickle


# Get Environment Vars
#openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")
os.environ["OPEN_API_KEY"] = config("OPEN_API_KEY")


# Initiate App
app = FastAPI()


# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]


# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    input_message: str
    #file: UploadFile = File(default=None, description="Upload a file")
    file: UploadFile = File(default=None)

# Check health
@app.get("/health")
async def check_health():
    return {"response": "healthy"}


@app.post("/bkp/chat-message/")
async def create_message(message: Message):
    # Perform any necessary operations with the received message
    # For example, you could store it in a database or process it in some way
    
    # Return a response indicating the successful creation of the message
    return {"message": "Message created successfully"}

# Post bot response
@app.post("/chat-message/")
async def post_audio(message: Message):

    input_message = message.input_message

    print(f"input_message => {message.input_message}")

    # Guard: Ensure output
    if not input_message:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(input_message)

    print(f"chat_response => {chat_response}")

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    return {"message": chat_response}


# Post bot response
@app.post("/chat/")
async def post_audio(message: Message):

    input_message = message.input_message

    print(f"input_message => {message.input_message}")

    # Guard: Ensure output
    if not input_message:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_summary_chain(input_message)

    print(f"chat_response => {chat_response}")

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    return {"message": chat_response}


@app.post("/upload")
async def upload_file(input_message: str, file: UploadFile = File(None)):
    input_question = input_message
    if file is not None:
        contents = await file.read()
        file_content = ""
        #For PDF
        if file.filename.lower().endswith(".pdf"):
            # Create a BytesIO object from the PDF content
            pdf_file = BytesIO(contents)
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Read the text content of each page in the PDF
            for page in pdf_reader.pages:
                file_content += page.extract_text()
        elif file.filename.lower().endswith(".txt"):
            file_content = contents.decode('utf-8')

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
        texts = text_splitter.split_text(text=file_content)

        store_name = file.filename[:-4]

        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
            print("Embeddings loaded from the disk")
        else:
            print("Embeddings loading from the upload")
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(texts, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)

        response = ""
    if input_question:
        docs = VectorStore.similarity_search(query=input_question, k=3)

        llm = OpenAI(temperature=0)
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=input_question)

    return response
