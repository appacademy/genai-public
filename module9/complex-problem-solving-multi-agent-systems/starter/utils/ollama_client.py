import os
import json
import requests
from typing import List, Dict, Any, Optional, Iterator, Union


class OllamaClient:
    """A client for interacting with the Ollama API."""

    def __init__(self, api_url: Optional[str] = None, model: str = "gemma3:4b"):
        """
        Initialize the Ollama client.

        Args:
            api_url: The URL of the Ollama API. If None, uses the OLLAMA_API_URL env variable.
            model: The default model to use for generation and embeddings.
        """
        self.api_url = api_url or os.getenv("OLLAMA_API_URL")
        if not self.api_url:
            raise ValueError(
                "Ollama API URL not provided and OLLAMA_API_URL environment variable not set"
            )
        self.model = model
        self.embedding_dimension = 384  # Default embedding dimension for gemma3:4b

    def check_health(self) -> bool:
        """
        Check if the Ollama API is available and responding.

        Returns:
            bool: True if the API is healthy, False otherwise.
        """
        try:
            health_check = requests.get(f"{self.api_url}/api/version", timeout=2)
            health_check.raise_for_status()
            return True
        except Exception as e:
            print(f"Ollama API health check failed: {e}")
            return False

    def print_health_message(self) -> None:
        """Print a formatted health check message if Ollama API is not available."""
        if not self.check_health():
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

    def generate(
        self,
        prompt: str,
        temperature: float = 0.8,
        stream: bool = False,
        model: Optional[str] = None,
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Generate a response from the Ollama model.

        Args:
            prompt: The prompt to send to the model.
            temperature: Controls randomness. Higher is more random.
            stream: Whether to stream the response.
            model: Optional override for the default model.

        Returns:
            Either a Dict containing the full response or an Iterator of response chunks if streaming
        """
        try:
            if not stream:
                response = requests.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": model or self.model,
                        "prompt": prompt,
                        "stream": stream,
                        "options": {"temperature": temperature},
                    },
                    timeout=60,
                )
                response.raise_for_status()
                return response.json()
            else:
                # Streaming response handling
                response = requests.post(
                    f"{self.api_url}/api/generate",
                    json={
                        "model": model or self.model,
                        "prompt": prompt,
                        "stream": stream,
                        "options": {"temperature": temperature},
                    },
                    stream=True,
                    timeout=120,  # Longer timeout for streaming
                )
                response.raise_for_status()

                # Create a generator to yield response chunks
                def generate_chunks():
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line.decode("utf-8"))
                                yield chunk
                            except json.JSONDecodeError:
                                pass

                return generate_chunks()

        except requests.exceptions.Timeout:
            # Handle timeout errors
            print("Request to Ollama API exceeded time limit.")
            error_response = {
                "response": """
                ⏱️ **Request Timed Out**
                
                The request to the Ollama API exceeded the allotted time. Possible causes include:
                
                1. The model is still initializing or processing a prior request
                2. The prompt is excessively large (consider reducing the number of comments)
                3. System resources are under strain
                
                Please retry with fewer comments or wait briefly before resubmitting.
                """,
                "prompt": prompt,
                "error": "Request timed out",
            }
            if stream:
                # Return a generator with a single error item for consistency
                def error_generator():
                    yield error_response

                return error_generator()
            else:
                return error_response

        except Exception as e:
            # Handle unexpected errors
            print(f"Error encountered: {e}")
            error_response = {
                "response": f"""
                ❌ **Error Generating Response**
                
                {str(e)}
                
                Please verify:
                - Ollama is operational with the {model or self.model} model
                - Network connectivity is stable
                - Sufficient system resources are available
                """,
                "prompt": prompt,
                "error": str(e),
            }
            if stream:
                # Return a generator with a single error item for consistency
                def error_generator():
                    yield error_response

                return error_generator()
            else:
                return error_response

    def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Get embedding vector for a text using Ollama API.

        Args:
            text: The text to embed.
            model: Optional override for the default model.

        Returns:
            List of floats representing the embedding vector.
        """
        try:
            # Instruction to get embeddings
            prompt = f"""Extract a numerical embedding vector that represents the semantic meaning of the following text. 
            Return ONLY a JSON array of {self.embedding_dimension} floating point numbers without any explanation or other text.
            
            TEXT: {text}"""

            response = requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": model or self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.0},
                },
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

            # Extract the array from the response
            response_text = result.get("response", "[]")

            # Clean up the response to ensure it's valid JSON
            cleaned_response = response_text.strip()
            if not cleaned_response.startswith("["):
                # Try to find the JSON array in the response
                start_idx = cleaned_response.find("[")
                end_idx = cleaned_response.rfind("]")
                if start_idx != -1 and end_idx != -1:
                    cleaned_response = cleaned_response[start_idx : end_idx + 1]
                else:
                    # If we can't find a proper array, return a default embedding
                    print("Could not parse embedding response, returning zeros")
                    return [0.0] * self.embedding_dimension

            try:
                embedding = json.loads(cleaned_response)
                # Ensure we have a properly sized embedding
                if isinstance(embedding, list) and len(embedding) > 0:
                    # Pad or truncate to ensure consistent size
                    if len(embedding) < self.embedding_dimension:
                        embedding.extend(
                            [0.0] * (self.embedding_dimension - len(embedding))
                        )
                    return embedding[: self.embedding_dimension]
                else:
                    print("Invalid embedding format, returning zeros")
                    return [0.0] * self.embedding_dimension
            except json.JSONDecodeError:
                print("Failed to parse embedding JSON, returning zeros")
                return [0.0] * self.embedding_dimension

        except Exception as e:
            print(f"Error getting embedding: {e}")
            # Return a vector of zeros as fallback
            return [0.0] * self.embedding_dimension

    def embed_documents(
        self, texts: List[str], model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Get embeddings for a list of texts.

        Args:
            texts: List of texts to embed.
            model: Optional override for the default model.

        Returns:
            List of embedding vectors.
        """
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text, model)
            embeddings.append(embedding)
        return embeddings

    def embed_query(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Get embedding for a single query text.

        Args:
            text: The query text to embed.
            model: Optional override for the default model.

        Returns:
            Embedding vector.
        """
        return self.get_embedding(text, model)


class OllamaEmbeddings:
    """
    A class that mimics the interface of language model embedding providers
    but uses Ollama under the hood.
    """

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        """
        Initialize the embeddings provider with an OllamaClient.

        Args:
            ollama_client: An existing OllamaClient instance. If None, creates a new one.
        """
        self.client = ollama_client or OllamaClient()
        # Check if the Ollama API is available
        self.client.print_health_message()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for a list of texts.

        Args:
            texts: List of texts to embed.

        Returns:
            List of embedding vectors.
        """
        return self.client.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Get embedding for a single query text.

        Args:
            text: The query text to embed.

        Returns:
            Embedding vector.
        """
        return self.client.get_embedding(text)
