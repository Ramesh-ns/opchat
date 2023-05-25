# uvicorn main:app
# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from pydantic import BaseModel
from functions.openai_requests import get_chat_response



# Get Environment Vars
#openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


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
# Note: Not playing back in browser when using post request.
@app.post("/chat-message/")
async def post_audio(message: Message):

    # Convert audio to text - production
    # Save the file temporarily
    # with open(file.filename, "wb") as buffer:
    #     buffer.write(file.file.read())
    # audio_input = open(file.filename, "rb")

    # # Decode audio
    # message_decoded = convert_audio_to_text(audio_input)

    message_decoded = message.input_message

    print(f"Decoded message => {message.input_message}")

    # Guard: Ensure output
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)

    print(f"chat_response => {chat_response}")

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    return {"message": chat_response}
