from fastapi import FastAPI, Body
from models import KeywordExtractRequest, MsgPayload
import os
from dotenv import load_dotenv
from utils.core import extract_keywords
import numpy as np


load_dotenv()
APP_NAME = os.getenv("APP_NAME", "FastAPI")
DEBUG = os.getenv("DEBUG", "False")

app = FastAPI()
messages_list: dict[int, MsgPayload] = {}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello"}


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}


# Route to add a message
@app.post("/messages/{msg_name}/")
def add_msg(msg_name: str) -> dict[str, MsgPayload]:
    # Generate an ID for the item based on the highest ID in the messages_list
    msg_id = max(messages_list.keys()) + 1 if messages_list else 0
    messages_list[msg_id] = MsgPayload(msg_id=msg_id, msg_name=msg_name)

    return {"message": messages_list[msg_id]}


# Route to list all messages
@app.get("/messages")
def message_items() -> dict[str, dict[int, MsgPayload]]:
    return {"messages:": messages_list}


@app.post("/api/extract_keywords")
def extract_keywordsextract_entities(request: KeywordExtractRequest):
    raw_input = [item.Title for item in request.data]
    results = extract_keywords(raw_input, request.category, request.min_freq)
    return {"results": results}