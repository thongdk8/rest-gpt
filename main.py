from typing import List
from fastapi import FastAPI, HTTPException
from openai import OpenAI
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel, Field
import os

app = FastAPI()

openaiKey = os.getenv("OPENAI_API_KEY")

if openaiKey is None:
    raise RuntimeError("No api key is provided")

# Initialize OpenAI client
client = OpenAI(api_key=openaiKey)


class Message(BaseModel):
    # An optional name for the participant
    name: str = Field(examples=['user_01'], default=None)

    # Based on the messages type from OpenAI we have sever roles as the examples
    role: str = Field(examples=['user', 'assistant',
                      'system', 'tool', 'function'], default='user')
    content: str = Field(examples=['Hello world'])


class ChatRequest(BaseModel):
    messages: List[Message] = Field()
    stream: bool = Field(default=True,
                         description="Enable stream for result or not, in case enabled the result will be return in form of Server-Sent Events")

    model: str = Field(examples=[
        "gpt-3.5-turbo",
        "gpt-4-0125-preview",
        "gpt-4-turbo-preview",
        "gpt-4-1106-preview",
        "gpt-4-vision-preview",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-16k-0613",
    ], default='gpt-3.5-turbo')

    # TODO: Add more options from OpenAI supported params e.g. temperature, top_p, ...


@app.post("/chat")
def chat(chat_request: ChatRequest):
    if (chat_request.messages.__len__() == 0):
        raise HTTPException(
            status_code=400, detail="Messages must be provided")

    chat_response = None
    try:
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_request.messages,
            stream=chat_request.stream
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to get response from OpenAI API: {}".format(str(e)))

    # Return full response if stream is disable
    if (chat_request.stream == False):
        return chat_response

    def event_generator():
        # loop the data to send event message
        for chunk in chat_response:
            yield {
                "event": "message",
                "data": chunk
            }

    return EventSourceResponse(event_generator())
