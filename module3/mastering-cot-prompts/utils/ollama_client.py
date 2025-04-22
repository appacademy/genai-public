"""
Ollama Client Module for interacting with the Ollama API.
Provides functionality to connect to and query the Gemma 3 4B model running locally.
"""

import requests
import json
from typing import Dict, List, Optional, Union
import time


class OllamaClient:
    """A client for interacting with the Ollama API with the Gemma 3 4B model."""

    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "gemma3:4b"
    ):
        """
        Initialize the Ollama client.

        Args:
            base_url (str): The base URL for the Ollama API. Default is "http://localhost:11434".
            model (str): The model to use for generation. Default is "gemma3:4b".
        """
        self.base_url = base_url
        self.model = model
        self.timeout = 60  # Default timeout in seconds

    def check_health(self) -> bool:
        """
        Check if the Ollama service is running and available.

        Returns:
            bool: True if Ollama is available, False otherwise.
        """
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=2)
            response.raise_for_status()
            return True
        except (
            requests.exceptions.RequestException,
            requests.exceptions.ConnectionError,
        ):
            return False

    def generate(
        self, prompt: str, temperature: float = 0.7, max_tokens: int = 1500
    ) -> Dict:
        """
        Generate a response using the Ollama API.

        Args:
            prompt (str): The prompt to send to the model.
            temperature (float): Controls randomness in generation. Default is 0.7.
            max_tokens (int): Maximum number of tokens to generate. Default is 1500.

        Returns:
            Dict: The parsed response from the Ollama API.
        """
        if not self.check_health():
            return {
                "error": "Ollama API not available",
                "message": "Please make sure Ollama is running with the gemma3:4b model.",
            }

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            }

            response = requests.post(
                f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {
                "error": "Request timed out",
                "message": "The request to the Ollama API timed out. The model might be still loading or the prompt is too complex.",
            }
        except Exception as e:
            return {
                "error": str(e),
                "message": f"An error occurred while generating a response: {str(e)}",
            }

    def chat_completion_format(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1500,
    ) -> Dict:
        """
        Format a ChatCompletion-style request (like OpenAI) for Ollama.

        Args:
            messages (List[Dict]): List of message dictionaries with 'role' and 'content' keys.
            temperature (float): Controls randomness in generation. Default is 0.7.
            max_tokens (int): Maximum number of tokens to generate. Default is 1500.

        Returns:
            Dict: Response formatted similar to OpenAI's ChatCompletion response.
        """
        # Convert the messages format to a single prompt for Ollama
        prompt = self._format_chat_messages(messages)

        # Generate response
        response = self.generate(prompt, temperature, max_tokens)

        # Check for error
        if "error" in response:
            return response

        # Format response to match OpenAI's format
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.get("response", ""),
                    },
                    "index": 0,
                }
            ],
            "model": self.model,
            "created": int(time.time()),
        }

    def _format_chat_messages(self, messages: List[Dict[str, str]]) -> str:
        """
        Format chat messages into a single prompt string.

        Args:
            messages (List[Dict]): List of message dictionaries with 'role' and 'content' keys.

        Returns:
            str: A formatted prompt string.
        """
        formatted_prompt = ""

        for message in messages:
            role = message.get("role", "").lower()
            content = message.get("content", "")

            if role == "system":
                formatted_prompt += f"SYSTEM: {content}\n\n"
            elif role == "user":
                formatted_prompt += f"USER: {content}\n\n"
            elif role == "assistant":
                formatted_prompt += f"ASSISTANT: {content}\n\n"
            else:
                # Handle other roles if needed
                formatted_prompt += f"{role.upper()}: {content}\n\n"

        formatted_prompt += "ASSISTANT: "
        return formatted_prompt
