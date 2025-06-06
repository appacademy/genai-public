from abc import ABC, abstractmethod
from typing import Dict, Any
import time
import re
from models.data_models import AgentResponse
from utils.ollama_client import OllamaClient


class Agent(ABC):
    def __init__(
        self, model: str = "gemma3:4b", temperature: float = 0.7, max_words: int = 1000
    ):
        self.model = model
        self.temperature = temperature
        self.max_words = max_words
        self.name = self.__class__.__name__
        self.ollama_client = OllamaClient()

    @abstractmethod
    def process(self, inputs: Dict[str, Any]) -> AgentResponse:
        """Process inputs and generate a response"""
        pass

    def _count_words(self, text: str) -> int:
        """Count the number of words in a text"""
        return len(re.findall(r"\b\w+\b", text))

    def _truncate_to_word_limit(self, text: str, max_words: int) -> str:
        """Truncate text to a maximum number of words"""
        words = re.findall(r"\S+|\n", text)
        if len(words) <= max_words:
            return text

        truncated = " ".join(words[:max_words])
        return truncated + f"\n\n[Note: Response truncated to {max_words} words]"

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Helper method to call the LLM with appropriate prompting and stream the output"""
        # Add balanced brevity instructions at the beginning of the system prompt
        brevity_instruction = f"""IMPORTANT INSTRUCTION: Provide a clear, well-structured response.
- Your response must be under {self.max_words} words total (maximum 1,000 words)
- Write in paragraph format with complete sentences
- Include sufficient detail to be informative and useful
- Focus on the most important information
- Provide thoughtful analysis rather than just listing points
- Maintain a professional, clear writing style
- Do not exceed {self.max_words} words

"""
        system_prompt = brevity_instruction + system_prompt

        full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"

        # Start streaming response
        ollama_response = self.ollama_client.generate(
            full_prompt,
            temperature=self.temperature,
            stream=True,
            model=self.model,
        )

        # Process streaming response
        response_parts = []
        chunk_buffer = []
        chunk_counter = 0

        for chunk in ollama_response:
            if "response" in chunk:
                chunk_text = chunk.get("response", "")
                response_parts.append(chunk_text)
                chunk_buffer.append(chunk_text)

                # Print progress indicator every few chunks
                chunk_counter += 1
                if chunk_counter % 5 == 0:
                    print("".join(chunk_buffer), end="", flush=True)
                    chunk_buffer.clear()

                # Allow for keyboard interrupt
                if chunk_counter % 20 == 0:
                    time.sleep(0.01)  # Small pause to allow for interrupts

        print(" done!\n")

        # Get the complete response
        complete_response = "".join(response_parts)

        # Enforce word limit by truncating if necessary
        word_count = self._count_words(complete_response)
        if word_count > self.max_words:
            print(
                f"⚠️ Response exceeded {self.max_words} words ({word_count}). Truncating..."
            )
            return self._truncate_to_word_limit(complete_response, self.max_words)

        return complete_response
