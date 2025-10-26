import logging
import os
import time
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
logger = logging.getLogger(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
grok_api_key = os.getenv("GROK_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

anthropic_url = "https://api.anthropic.com/v1/"
gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
groq_url = "https://api.groq.com/openai/v1"
grok_url = "https://api.x.ai/v1"
openrouter_url = "https://openrouter.ai/api/v1"
ollama_url = "http://localhost:11434/v1"

openai_client = OpenAI(api_key=openai_api_key)
anthropic_client = OpenAI(api_key=anthropic_api_key, base_url=anthropic_url)
gemini_client = OpenAI(api_key=google_api_key, base_url=gemini_url)
groq_client = OpenAI(api_key=groq_api_key, base_url=groq_url)
grok_client = OpenAI(api_key=grok_api_key, base_url=grok_url)
openrouter_client = OpenAI(base_url=openrouter_url, api_key=openrouter_api_key)


def get_response(
    model: str,
    messages: List[Dict[str, str]],
    retry_count: int = 2,
    sleep_time: float = 1.0,
) -> Optional[str]:
    """
    Gets a chat completion response with simple retry logic.

    Args:
        client (openai.OpenAI): OpenAI client instance.
        model (str): Model name (e.g., "gpt-4o-mini").
        messages (List[Dict[str, str]]): Chat messages for the request.
        retry_count (int, optional): Number of retry attempts. Defaults to 2.
        sleep_time (int, optional): Seconds to wait between retries. Defaults to 1.

    Returns:
        str | None: The model's response text, or None if all retries fail.
    """
    if model == "gpt-4o-mini":
        client = openai_client
    elif model == "gpt-5-mini":
        client = openai_client
    elif model == "claude-3-5-haiku-latest":
        client = anthropic_client
    elif model == "claude-3-5-sonnet-latest":
        client = anthropic_client
    elif model == "gemini-2.5-pro":
        client = gemini_client
    elif model == "gemini-2.5-flash-lite":
        client = gemini_client
    elif model == "llama-3.1-8b-instant":
        client = groq_client
    elif model == "llama-3.3-70b-versatile":
        client = groq_client
    elif model == "kimi-k2-instruct-0905":
        client = groq_client
    elif model == "z-ai/glm-4.5":
        client = groq_client
    else:
        raise ValueError(f"Invalid model: {model}")

    for attempt in range(1, retry_count + 1):
        try:
            response = client.chat.completions.create(model=model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            is_last = attempt == retry_count
            logger.error(
                "Error getting response from %s (attempt %d/%d): %s",
                model,
                attempt,
                retry_count,
                e,
            )
            if is_last:
                raise
            time.sleep(sleep_time)

    return None
