import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

LLM_SMART_KEYWORD = os.getenv("LLM_SMART_KEYWORD", "")

def call_llm_keyword_filter(category, keywords):
    """
    Call LLM API to filter keywords by category.

    Args:
        category (str): Category name (e.g., "banking")
        keywords (list): List of keyword strings

    Returns:
        dict or list: Parsed JSON response from API
    """

    payload = json.dumps({
        "category": category,
        "keywords": keywords
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(LLM_SMART_KEYWORD, headers=headers, data=payload, timeout=30)
        response.raise_for_status()  # Raise error if HTTP error
        return response.json()  # Return as parsed JSON
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None
