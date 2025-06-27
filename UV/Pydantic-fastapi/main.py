from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field 
from datetime import datetime, UTC # For handling datetime in UTC
from uuid import uuid4  # For generating unique IDs

# Initialize FastAPI app
app = FastAPI(
    title="Custom Chat Bot",
    description="An FastAPI application for a custom chat bot with Pydantic validation.",
    version="0.1.0"
)
# Complex Custom Pydantic model for chat messages
class MetaData(BaseModel):
    """Metadata for chat messages."""
     # Default current UTC time creatted at every request by pydantic. as it will call this lambda function
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Timestamp of the message in UTC")
     # Pydantic Generates a unique user ID by calling this lambda function, then converts it to a string. 
    session_id: str = Field(default_factory=lambda: str(uuid4())) # works fine without description

class ChatMessage(BaseModel):
    """Model for chat messages."""
    user_id: str #= Field(..., description="Unique identifier for the user")
    message: str #= Field(..., description="The content of the chat message")
    metadata: MetaData #= Field(default_factory=MetaData, description="Metadata associated with the chat message")    

class ChatResponse(BaseModel):
    """Model for chat responses."""
    user_id: str #= Field(..., description="Unique identifier for the user")
    response: str #= Field(..., description="The response from the chat bot")
    metadata: MetaData #= Field(default_factory=MetaData, description="Metadata associated with the chat response")    

# Root endpoint
@app.get("/", tags=["Root"]) 
async def read_root(): 
    """Root endpoint.""" # the entry point for the API when accessed via a GET request to the base URL
    return {"message": "Welcome to the Custom Chat Bot API!"}

# Get Endpoint for Querry Parameters
@app.get("/users/{user_id}") # Path parameter for user_id
async def get_user(user_id: str, role: str | None = None): # Optional query parameter for role
    user_info = {"user_id": user_id, role: role if role else "Guest"} # Default role is "Guest" if not provided
    return user_info # Return user information as a dictionary

# Post Endpoint for Chat Messages
@app.post("/chat/", response_model=ChatResponse) # Endpoint to create a chat message
async def chat(chat_message: ChatMessage):
    """Endpoint to create a chat message."""
    # Here you would typically process the chat message, e.g., save it to a database or pass it to a chat bot service
    # For this example, we will just return the same message as a response
    if not chat_message.text.strip(): # Check if the message is empty
        raise HTTPException(status_code=400, detail="Message cannot be empty") # Raise an error if the message is empty
    reply_text = f"Hello, {ChatMessage.user_id}! You said: '{ChatMessage.text}'. How can I assist you today?"
    # Create a response object with the same user_id and message, and include metadata
    response = ChatResponse(
        user_id=chat_message.user_id,
        response=reply_text,
        metadata=chat_message.metadata
    )
    return response