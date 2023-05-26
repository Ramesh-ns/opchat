# uvicorn main:app
# uvicorn main:app --reload

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from pydantic import BaseModel
from openai_requests.openai_requests import get_chat_response
from langchain_requests.custom_chains import get_summary_chain



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
