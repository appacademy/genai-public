from typing import List, Dict, Any


class PromptTemplate:
    """A structured template for creating prompts using the five-part framework."""

    def __init__(
        self,
        context: str = "",
        instruction: str = "",
        response_format: str = "",
        constraints: str = "",
        examples: List[Dict[str, str]] = None,
    ):
        self.context = context
        self.instruction = instruction
        self.response_format = response_format
        self.constraints = constraints
        self.examples = examples or []
        self.version = 1

    def get_full_prompt(self) -> str:
        """Combine all components into a complete prompt."""
        prompt_parts = []

        if self.context:
            prompt_parts.append(f"# Context\n{self.context}\n")

        if self.instruction:
            prompt_parts.append(f"# Instruction\n{self.instruction}\n")

        if self.response_format:
            prompt_parts.append(f"# Response Format\n{self.response_format}\n")

        if self.constraints:
            prompt_parts.append(f"# Constraints\n{self.constraints}\n")

        if self.examples:
            prompt_parts.append("# Examples")
            for example in self.examples:
                prompt_parts.append(
                    "\n## Input\n" + example.get("query", example.get("input", ""))
                )
                prompt_parts.append(
                    "\n## Expected Output\n"
                    + example.get("response", example.get("output", ""))
                )

        return "\n".join(prompt_parts)

    def validate(self) -> bool:
        """Check if the prompt has the necessary components."""
        # Basic validation: instruction is the only required field
        if not self.instruction:
            return False
        return True

    def update_version(self):
        """Increment the version number when the prompt is modified."""
        self.version += 1
        return self.version

    def to_dict(self) -> Dict[str, Any]:
        """Convert the template to a dictionary for storage."""
        return {
            "context": self.context,
            "instruction": self.instruction,
            "response_format": self.response_format,
            "constraints": self.constraints,
            "examples": self.examples,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptTemplate":
        """Create a template from a dictionary."""
        template = cls(
            context=data.get("context", ""),
            instruction=data.get("instruction", ""),
            response_format=data.get("response_format", ""),
            constraints=data.get("constraints", ""),
            examples=data.get("examples", []),
        )
        template.version = data.get("version", 1)
        return template
