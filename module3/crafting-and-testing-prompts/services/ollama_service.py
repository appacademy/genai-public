import requests
import time
import logging
from typing import Dict, Any, Optional, List
from .mock_llm_service import MockLLMService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("OllamaService")


class OllamaService:
    """Service for interacting with Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.mock_service = MockLLMService()
        self.is_available = self._check_availability()
        # Log whether Ollama is available
        if self.is_available:
            logger.info("Ollama service is available")
        else:
            logger.warning("Ollama service is not available, will use mock service")

    def _check_availability(self) -> bool:
        """Check if Ollama service is available."""
        try:
            logger.info(f"Checking Ollama availability at {self.base_url}/api/tags")
            response = requests.get(
                f"{self.base_url}/api/tags", timeout=5
            )  # Increased timeout
            available = response.status_code == 200
            if available:
                # Log the available models
                models = [
                    model.get("name") for model in response.json().get("models", [])
                ]
                logger.info(f"Available Ollama models: {models}")
            else:
                logger.warning(
                    f"Ollama API returned status code: {response.status_code}"
                )
            return available
        except Exception as e:
            logger.error(f"Error checking Ollama availability: {str(e)}")
            return False

    def _get_available_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return [
                    model.get("name", "") for model in response.json().get("models", [])
                ]
            return []
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []

    def _find_matching_model(
        self, requested_model: str, available_models: List[str]
    ) -> Optional[str]:
        """Try to find a matching model from available models."""
        if not available_models:
            return None

        # Direct match
        if requested_model in available_models:
            return requested_model

        # Try with different formatting (handles gemma:3-4b vs gemma3:4b)
        normalized_requested = requested_model.replace("-", "").replace(":", "")

        for model in available_models:
            normalized_model = model.replace("-", "").replace(":", "")
            if normalized_requested == normalized_model:
                return model

            # Check if it's the same base model (e.g., "gemma" part of "gemma:3-4b")
            requested_base = (
                requested_model.split(":")[0]
                if ":" in requested_model
                else requested_model
            )
            model_base = model.split(":")[0] if ":" in model else model

            if requested_base == model_base:
                logger.info(f"Found matching base model: {model} for {requested_model}")
                return model

        return None

    def generate(
        self,
        prompt: str,
        model: str = "gemma:3-4b",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        force_real_llm: bool = False,  # Default to False to allow fallback
    ) -> Dict[str, Any]:
        """Generate a response from Ollama, or use mock service if Ollama is unavailable."""
        # If Ollama is not available and we're not forcing real LLM, use the mock service
        if not self.is_available and not force_real_llm:
            logger.info(f"Using mock service for prompt: {prompt[:50]}...")
            return self.mock_service.generate(prompt, model, temperature, max_tokens)

        # If we're forcing real LLM but Ollama is not available, try to check again
        if not self.is_available and force_real_llm:
            logger.info("Forcing use of real LLM, rechecking Ollama availability")
            self.is_available = self._check_availability()
            if not self.is_available:
                logger.error("Still unable to connect to Ollama after recheck")
                if not force_real_llm:
                    logger.info("Falling back to mock service")
                    return self.mock_service.generate(
                        prompt, model, temperature, max_tokens
                    )
                # If we're still forcing, we'll try anyway

        start_time = time.time()
        logger.info(
            f"Generating response with model '{model}' for prompt: {prompt[:50]}..."
        )

        try:
            # Attempt to map the model name to what's available in Ollama
            available_models = self._get_available_models()
            logger.info(f"Models available for mapping: {available_models}")

            # Try to find a matching model by performing some normalization
            model_name = self._find_matching_model(model, available_models)

            if not model_name and force_real_llm:
                # If we couldn't find a match but forcing real LLM, use original name as a fallback
                logger.warning(f"No matching model found for '{model}', using as-is")
                model_name = model
            elif not model_name:
                # If we couldn't find a match and not forcing, use mock
                logger.warning(
                    f"No matching model found for '{model}', falling back to mock"
                )
                return self.mock_service.generate(
                    prompt, model, temperature, max_tokens
                )

            logger.info(f"Selected model name: '{model_name}' (original: '{model}')")

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
                timeout=120,  # Increased timeout for longer responses
            )

            # Log status code
            logger.info(f"Ollama API response status code: {response.status_code}")

            response.raise_for_status()
            result = response.json()

            # Format the response to match our expected structure
            formatted_response = {
                "response": result.get("response", ""),
                "response_time": time.time() - start_time,
                "estimated_prompt_tokens": self._estimate_tokens(prompt),
                "estimated_completion_tokens": self._estimate_tokens(
                    result.get("response", "")
                ),
            }

            formatted_response["estimated_total_tokens"] = (
                formatted_response["estimated_prompt_tokens"]
                + formatted_response["estimated_completion_tokens"]
            )

            logger.info(
                f"Successfully generated response ({len(formatted_response['response'])} chars)"
            )
            return formatted_response
        except Exception as e:
            logger.error(f"Error connecting to Ollama: {str(e)}")
            # For debugging, show detailed exception
            logger.error(f"Exception type: {type(e).__name__}")

            # If not forcing real LLM, fall back to mock service
            if not force_real_llm:
                logger.info("Falling back to mock service")
                return self.mock_service.generate(
                    prompt, model, temperature, max_tokens
                )
            else:
                # Re-raise the exception if forcing real LLM
                logger.error(
                    "Force real LLM is enabled, not falling back to mock service"
                )
                raise

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count based on text length."""
        # Rough estimate: ~4 characters per token for English text
        return len(text) // 4
