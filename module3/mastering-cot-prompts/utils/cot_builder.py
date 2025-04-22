import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from utils.ollama_client import OllamaClient


class ChainOfThoughtBuilder:
    """A tool for building chain-of-thought reasoning prompts for LLMs."""

    def __init__(self):
        # Initialize Ollama client
        self.ollama_client = OllamaClient()

        # Define reasoning templates
        self.reasoning_templates = {
            "sequential": {
                "description": "Step-by-step problem solving",
                "structure": [
                    "First, understand the problem by identifying key elements.",
                    "Second, break down the problem into manageable parts.",
                    "Third, address each part systematically.",
                    "Finally, integrate the solutions for a comprehensive answer.",
                ],
            },
            "criteria_based": {
                "description": "Evaluating against multiple criteria",
                "structure": [
                    "Identify all relevant criteria for evaluation.",
                    "For each criterion, assess how the subject measures up.",
                    "Weigh the importance of different criteria.",
                    "Form an overall conclusion based on the criteria assessment.",
                ],
            },
            "comparative": {
                "description": "Analyzing pros and cons",
                "structure": [
                    "Identify all options or approaches being compared.",
                    "For each option, list its advantages (pros).",
                    "For each option, list its disadvantages (cons).",
                    "Compare the options based on their pros and cons.",
                    "Recommend the best option with justification.",
                ],
            },
        }

        # Define domain-specific templates
        self.domain_templates = {
            "code_analysis": {
                "context": "You are a senior software developer analyzing code for improvements.",
                "instruction_template": "Analyze the following code snippet:\n{problem}",
                "constraints": [
                    "Focus on both functionality and code quality",
                    "Consider performance implications",
                    "Suggest specific improvements with code examples",
                ],
                "example": {
                    "problem": "def find_max(nums):\n    max_val = nums[0]\n    for i in range(len(nums)):\n        if nums[i] > max_val:\n            max_val = nums[i]\n    return max_val",
                    "reasoning": "I'll analyze this code step by step:\n1. First, I need to understand what the function does: it finds the maximum value in a list.\n2. The code initializes max_val to the first element, then loops through all elements to find larger values.\n3. The logic is correct, but there's an inefficiency: the loop starts from index 0, but we've already assigned nums[0] to max_val.\n4. Also, there's no error handling for empty lists.\n\nSuggested improvements:\n\n```python\ndef find_max(nums):\n    if not nums:  # Handle empty list\n        raise ValueError(\"Cannot find maximum of empty list\")\n    max_val = nums[0]\n    for i in range(1, len(nums)):  # Start from second element\n        if nums[i] > max_val:\n            max_val = nums[i]\n    return max_val\n```\n\nAlternatively, Python has a built-in max() function that would be more efficient:\n\n```python\ndef find_max(nums):\n    if not nums:\n        raise ValueError(\"Cannot find maximum of empty list\")\n    return max(nums)\n\n```",
                },
            },
            "hr_policy": {
                "context": "You are an HR specialist determining how company policies apply to specific situations.",
                "instruction_template": "Analyze how company policies apply to this situation: \n\n{problem}",
                "constraints": [
                    "Consider both the letter and spirit of company policies",
                    "Ensure fair and consistent application of rules",
                    "Balance company requirements with employee needs",
                    "Consider any legal compliance issues",
                ],
                "example": {
                    "problem": "An employee has requested two consecutive weeks of vacation during the company's busiest season. The company policy states employees can take up to three weeks of vacation per year with manager approval.",
                    "reasoning": "I'll analyze this HR scenario step by step:\n\n1. First, I need to identify the relevant policies: The company allows up to 3 weeks vacation annually with manager approval.\n\n2. Next, I'll evaluate policy constraints: The request is within the 3-week annual limit, but timing is during the busiest season.\n\n3. Now I'll consider competing interests:\n   - Employee interests: Time off for rest, personal matters, or planned events\n   - Company interests: Maintaining operations during peak business periods\n   - Legal considerations: Employees are entitled to use their benefits, but companies can reasonably manage timing\n\n4. Possible approaches:\n   - Deny the request outright (high risk of employee dissatisfaction)\n   - Approve the request despite business impact (operational risk)\n   - Negotiate a compromise (partial approval, alternative timing, or staggered approach)\n\n5. Recommendation: The manager should meet with the employee to discuss:\n   - The business impact of the timing\n   - Whether partial approval is possible (e.g., one week now, one later)\n   - Alternative dates that would work better for the business\n   - The employee's specific needs to see if accommodations can be made\n\nThis approach respects the employee's right to use their benefits while acknowledging the company's operational needs, finding a balance that treats the employee fairly while protecting business interests.",
                },
            },
        }

    def update_template(self, template_type, template_name, new_data):
        """Update a reasoning template or domain template with new data."""
        if template_type == "reasoning":
            if template_name in self.reasoning_templates:
                self.reasoning_templates[template_name].update(new_data)
        elif template_type == "domain":
            if template_name in self.domain_templates:
                self.domain_templates[template_name].update(new_data)

    def add_template(self, template_type, template_name, template_data):
        """Add a new reasoning template or domain template."""
        if template_type == "reasoning":
            # Create a deep copy to ensure we're not modifying by reference
            self.reasoning_templates[template_name] = dict(template_data)
            # Print confirmation for debugging
            print(f"Added reasoning template: {template_name}")
            # Print the current templates for debugging
            print(
                f"Current reasoning templates: {list(self.reasoning_templates.keys())}"
            )
        elif template_type == "domain":
            # Create a deep copy to ensure we're not modifying by reference
            self.domain_templates[template_name] = dict(template_data)
            # Print confirmation for debugging
            print(f"Added domain template: {template_name}")
            # Print the current templates for debugging
            print(f"Current domain templates: {list(self.domain_templates.keys())}")

    def build_cot_prompt(
        self,
        problem_description: str,
        domain: str,
        reasoning_type: str,
        examples: Optional[List[Dict]] = None,
        custom_sections: Optional[Dict] = None,
    ) -> str:
        """
        Build a chain-of-thought prompt using the five-part structure.

        Args:
            problem_description: The specific problem to solve
            domain: Domain area (code_analysis, hr_policy, custom)
            reasoning_type: Type of reasoning (sequential, criteria_based, comparative)
            examples: Optional examples for few-shot learning
            custom_sections: Optional dictionary to override default sections

        Returns:
            A structured prompt string
        """
        # Use custom sections if provided, otherwise use defaults
        if custom_sections is None:
            custom_sections = {}

        # 1. Context
        context = custom_sections.get(
            "context", self.domain_templates[domain]["context"]
        )

        # 2. Instruction
        instruction_template = custom_sections.get(
            "instruction_template",
            self.domain_templates[domain]["instruction_template"],
        )

        # Format the problem description based on domain
        if domain == "code_analysis":
            # Check if problem description contains code (triple backticks)
            if "```" in problem_description:
                # Use the problem description as is, preserving code formatting
                instruction = instruction_template.format(problem=problem_description)
            else:
                # Check if the problem description looks like code without backticks
                code_indicators = [
                    "def ",
                    "class ",
                    "function",
                    "import ",
                    "for ",
                    "if ",
                    "while ",
                    "return ",
                    "var ",
                    "let ",
                    "const ",
                ]
                might_be_code = any(
                    indicator in problem_description for indicator in code_indicators
                )

                if might_be_code and not problem_description.strip().startswith("```"):
                    # Wrap the problem in code blocks if it looks like code
                    formatted_problem = f"```python\n{problem_description}\n```"
                    instruction = instruction_template.format(problem=formatted_problem)
                else:
                    # Use as normal text
                    instruction = instruction_template.format(
                        problem=problem_description
                    )
        else:
            # For other domains, use normal text formatting
            instruction = instruction_template.format(problem=problem_description)

        # Add chain-of-thought guidance
        cot_steps = custom_sections.get(
            "cot_steps", self.reasoning_templates[reasoning_type]["structure"]
        )
        cot_guidance = "\n".join([f"- {step}" for step in cot_steps])
        instruction += (
            f"\n\nUse the following chain-of-thought approach:\n{cot_guidance}"
        )

        # 3. Format
        format_instruction = custom_sections.get(
            "format_instruction",
            "Please provide your analysis in a clear, step-by-step format. For each step, explain your reasoning thoroughly.",
        )

        # 4. Constraints
        constraints = custom_sections.get(
            "constraints", self.domain_templates[domain]["constraints"]
        )
        constraints_text = "\n".join([f"- {constraint}" for constraint in constraints])

        # 5. Examples (few-shot)
        examples_text = ""
        if examples:
            # Use provided examples
            for example in examples:
                examples_text += f"\nExample Problem: \n\n{example['problem']}\n\nStep-by-step solution: {example['reasoning']}\n"
        elif (
            "example" in self.domain_templates[domain]
            and self.domain_templates[domain]["example"]
        ):
            # Use the default example for this domain
            example = self.domain_templates[domain]["example"]
            examples_text = f"\nExample Problem: \n\n{example['problem']}\n\nStep-by-step solution: {example['reasoning']}\n"

        # Combine all parts
        prompt = f"""# Context
{context}

# Instruction
{instruction}

# Output Format
{format_instruction}

# Constraints
Please adhere to these constraints:
{constraints_text}

# Examples
{examples_text}
"""
        return prompt

    def execute_prompt(self, prompt: str, model: str = "gemma3:4b") -> str:
        """Send the prompt to the Ollama API and get the response."""
        try:
            # Ignore the model parameter from the UI and use Gemma3 model
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant that provides detailed chain-of-thought reasoning.",
                },
                {"role": "user", "content": prompt},
            ]
            response = self.ollama_client.chat_completion_format(
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )

            # Check if there was an error with Ollama
            if "error" in response:
                return (
                    f"Error: {response.get('message', 'Unknown error with Ollama API')}"
                )

            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"

    def compare_with_standard_prompt(
        self, problem_description: str, domain: str, model: str = "gemma3:4b"
    ) -> Dict:
        """Compare results between standard and CoT prompting."""
        # Create a standard prompt (without chain-of-thought)
        standard_prompt = f"""You are an AI assistant specializing in {domain.replace('_', ' ')}. 
        
Please analyze the following:

{problem_description}

Provide your analysis and recommendations."""

        # Create a chain-of-thought prompt
        cot_prompt = self.build_cot_prompt(problem_description, domain, "sequential")

        # Execute both prompts
        standard_response = self.execute_prompt(standard_prompt, model)
        cot_response = self.execute_prompt(cot_prompt, model)

        # Simple analysis of differences
        std_word_count = len(standard_response.split())
        cot_word_count = len(cot_response.split())
        word_diff = cot_word_count - std_word_count

        # Look for reasoning indicators in responses
        reasoning_indicators = [
            "first",
            "second",
            "third",
            "next",
            "finally",
            "because",
            "therefore",
            "thus",
            "step",
            "consider",
        ]
        std_indicators = sum(
            1
            for indicator in reasoning_indicators
            if indicator.lower() in standard_response.lower()
        )
        cot_indicators = sum(
            1
            for indicator in reasoning_indicators
            if indicator.lower() in cot_response.lower()
        )

        analysis = f"""
Comparison Analysis:
- Standard response: {std_word_count} words, {std_indicators} reasoning indicators
- CoT response: {cot_word_count} words, {cot_indicators} reasoning indicators
- Difference: CoT response is {word_diff} words longer with {cot_indicators - std_indicators} more reasoning indicators

The Chain-of-Thought prompt appears to have generated a {'more detailed, structured response' if cot_word_count > std_word_count and cot_indicators > std_indicators else 'similar response to the standard prompt'}.
"""

        # Highlight reasoning indicators in responses
        highlighted_standard = standard_response
        highlighted_cot = cot_response

        for indicator in reasoning_indicators:
            highlighted_standard = highlighted_standard.replace(
                indicator.capitalize(), f"**{indicator.capitalize()}**"
            ).replace(f" {indicator} ", f" **{indicator}** ")

            highlighted_cot = highlighted_cot.replace(
                indicator.capitalize(), f"**{indicator.capitalize()}**"
            ).replace(f" {indicator} ", f" **{indicator}** ")

        return {
            "standard_prompt": standard_prompt,
            "standard_response": standard_response,
            "highlighted_standard_response": highlighted_standard,
            "cot_prompt": cot_prompt,
            "cot_response": cot_response,
            "highlighted_cot_response": highlighted_cot,
            "analysis": analysis,
            "metrics": {
                "standard_word_count": std_word_count,
                "cot_word_count": cot_word_count,
                "standard_reasoning_indicators": std_indicators,
                "cot_reasoning_indicators": cot_indicators,
            },
        }

    def save_results(self, results: Dict, filename: str = None):
        """Save prompt comparison results to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cot_comparison_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(results, f, indent=2)

        return f"Results saved to {filename}"

    def get_template_info(self, template_type, template_name):
        """Get detailed information about a specific template."""
        if template_type == "reasoning":
            return self.reasoning_templates.get(template_name, {})
        elif template_type == "domain":
            return self.domain_templates.get(template_name, {})
        return {}
