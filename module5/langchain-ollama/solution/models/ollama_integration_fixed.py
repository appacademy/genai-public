"""
Fixed Ollama Integration for LangChain

This module provides a LangChain-compatible wrapper for the Ollama API client
with improved error handling and timeouts.
"""

from typing import Any, Dict, List, Optional, Union, Mapping, Callable
import os
import requests
import json
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from pydantic import Field


class OllamaLLM(LLM):
    """
    LangChain-compatible wrapper for Ollama models with improved error handling.

    This class provides an interface for using Ollama models with LangChain,
    supporting both streaming and non-streaming modes.
    """

    # Define class attributes as Pydantic fields
    model_name: str = "gemma3:4b"
    temperature: float = 0.0
    api_url: Optional[str] = None
    timeout: int = 120
    debug_prompts: bool = False
    debug_stream: bool = False

    def __init__(
        self,
        model_name: str = "gemma3:4b",
        temperature: float = 0.0,
        api_url: Optional[str] = None,
        timeout: int = 120,
        debug_prompts: bool = False,
        debug_stream: bool = False,
        **kwargs,
    ):
        """
        Initialize the Ollama LLM.

        Args:
            model_name: The name of the Ollama model to use. Defaults to "gemma3:4b".
            temperature: Controls randomness. Higher is more random. Defaults to 0.0.
            api_url: The URL of the Ollama API. If None, uses the OLLAMA_API_URL env variable.
            timeout: Timeout in seconds for API requests. Defaults to 120.
            debug_prompts: If True, prints all prompts sent to the API.
            debug_stream: If True, prints all chunks received from streaming responses.
            **kwargs: Additional keyword arguments to pass to the parent class.
        """
        # Initialize with the fields
        kwargs_with_fields = {
            "model_name": model_name,
            "temperature": temperature,
            "api_url": api_url or os.getenv("OLLAMA_API_URL", "http://localhost:11434"),
            "timeout": timeout,
            "debug_prompts": debug_prompts,
            "debug_stream": debug_stream,
            **kwargs,
        }

        # Initialize the parent class
        super().__init__(**kwargs_with_fields)

        # Check if Ollama API is available
        self._check_api_health()

    def _check_api_health(self) -> bool:
        """
        Check if the Ollama API is available and responding.

        Returns:
            bool: True if the API is healthy, False otherwise.
        """
        try:
            print(f"Checking Ollama API health at {self.api_url}...")
            health_check = requests.get(f"{self.api_url}/api/version", timeout=5)
            health_check.raise_for_status()
            print(f"Ollama API is healthy! Version: {health_check.text}")
            return True
        except Exception as e:
            print(f"Ollama API health check failed: {e}")
            print(
                """
            ⚠️ **Ollama API Unavailable**
            
            The Ollama service is not currently operational. To resolve this:
            
            1. Open a terminal and execute: `ollama run gemma3:4b`
            2. Allow the model to fully initialize
            3. Resubmit your question
            
            If Ollama is already active in another terminal, confirm it remains operational.
            """
            )
            return False

    @property
    def _llm_type(self) -> str:
        """Return the type of LLM."""
        return "ollama"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> str:
        """
        Call the Ollama model with the given prompt.

        Args:
            prompt: The prompt to send to the model.
            stop: A list of strings to stop generation when encountered.
            run_manager: A callback manager for the LLM run.
            **kwargs: Additional keyword arguments.

        Returns:
            The generated text.
        """
        # Override temperature if provided
        temperature = kwargs.get("temperature", self.temperature)

        # Debug: Print prompt if enabled
        if self.debug_prompts:
            print("\n" + "=" * 80)
            print(f"PROMPT TO {self.model_name.upper()}:")
            print("-" * 80)
            print(prompt)
            print("=" * 80 + "\n")

        try:
            # Prepare the payload
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            }

            # Make the request
            print(f"Sending request to Ollama API at {self.api_url}...")
            response = requests.post(
                f"{self.api_url}/api/generate", json=payload, timeout=self.timeout
            )
            response.raise_for_status()

            # Parse the response
            result = response.json()

            # Debug: Print response if enabled
            if self.debug_stream:
                print("\n" + "=" * 80)
                print(f"RESPONSE FROM {self.model_name.upper()}:")
                print("-" * 80)
                print(result.get("response", "No response"))
                print("=" * 80 + "\n")

            return result.get("response", "")

        except requests.exceptions.Timeout:
            error_msg = f"Request to Ollama API timed out after {self.timeout} seconds."
            print(error_msg)
            return error_msg

        except Exception as e:
            error_msg = f"Error generating response: {e}"
            print(error_msg)
            return error_msg

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ) -> Any:
        """
        Stream the response from the Ollama model for the given prompt.

        Args:
            prompt: The prompt to send to the model.
            stop: A list of strings to stop generation when encountered.
            run_manager: A callback manager for the LLM run.
            **kwargs: Additional keyword arguments.

        Yields:
            Chunks of the generated text.
        """
        # Override temperature if provided
        temperature = kwargs.get("temperature", self.temperature)

        # Debug: Print prompt if enabled
        if self.debug_prompts:
            print("\n" + "=" * 80)
            print(f"PROMPT TO {self.model_name.upper()} (STREAMING):")
            print("-" * 80)
            print(prompt)
            print("=" * 80 + "\n")

        try:
            # Prepare the payload
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True,
                "options": {"temperature": temperature},
            }

            # Make the request
            print(f"Sending streaming request to Ollama API at {self.api_url}...")
            response = requests.post(
                f"{self.api_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()

            # Process the streaming response
            if self.debug_stream:
                print("\n" + "=" * 80)
                print(f"STREAMING RESPONSE FROM {self.model_name.upper()}:")
                print("-" * 80)

            # Process the streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            text_chunk = chunk["response"]

                            # Debug: Print streaming chunks if enabled
                            if self.debug_stream:
                                print(text_chunk, end="", flush=True)

                            if run_manager:
                                run_manager.on_llm_new_token(text_chunk)

                            yield GenerationChunk(text=text_chunk)
                    except json.JSONDecodeError as e:
                        error_msg = f"Error decoding JSON from stream: {e}" # Removed DEBUG prefix
                        print(error_msg) 
                        yield GenerationChunk(text=error_msg)

            if self.debug_stream:
                print("\n" + "=" * 80)

        except requests.exceptions.Timeout:
            error_msg = f"Streaming request to Ollama API timed out after {self.timeout} seconds."
            print(error_msg)
            yield GenerationChunk(text=error_msg)

        except Exception as e:
            error_msg = f"Error streaming response: {e}"
            print(error_msg)
            yield GenerationChunk(text=error_msg)
