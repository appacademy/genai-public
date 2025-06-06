import json


class KnowledgeBase:
    """Loads and manages context information for different inquiry types."""

    def __init__(self, context_dir="context"):
        """Initialize the knowledge base by loading context files."""
        self.context_dir = context_dir
        self.contexts = {}
        self.load_all_contexts()

    def load_all_contexts(self):
        """Load all context files from the context directory."""
        context_types = ["billing", "technical", "product", "general", "priority"]
        for context_type in context_types:
            self.contexts[context_type] = self.load_context(context_type)

    def load_context(self, context_type):
        """Load a specific context file."""
        try:
            with open(f"{self.context_dir}/{context_type}_context.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Context file for {context_type} not found")
            return {"policies": [], "common_issues": {}, "faqs": []}

    def get_context_for_prompt(self, context_type, issue_type=None):
        """Format context information for inclusion in a prompt."""
        context = self.contexts.get(context_type, {})

        # Start with policies
        formatted_context = "COMPANY POLICIES:\n"
        for policy in context.get("policies", []):
            formatted_context += f"- {policy}\n"

        # Add common issues if an issue type is specified
        if issue_type and issue_type in context.get("common_issues", {}):
            formatted_context += f"\nRECOMMENDED APPROACH FOR {issue_type.upper()}:\n"
            formatted_context += context["common_issues"][issue_type] + "\n"

        # Add general approach for handling this type of inquiry
        formatted_context += "\nCOMMON ISSUES AND APPROACHES:\n"
        for issue, approach in list(context.get("common_issues", {}).items())[
            :3
        ]:  # Include a few examples
            if issue != issue_type:  # Skip the one we already included
                formatted_context += f"- {issue}: {approach}\n"

        # Add FAQs for reference
        formatted_context += "\nRELEVANT FAQs:\n"
        for faq in context.get("faqs", [])[:3]:  # Include a few examples
            formatted_context += f"Q: {faq['question']}\nA: {faq['answer']}\n\n"

        # Add special sections based on context type
        if context_type == "product" and "product_tiers" in context:
            formatted_context += "\nPRODUCT TIERS:\n"
            for tier, details in context["product_tiers"].items():
                formatted_context += (
                    f"- {tier}: {details['price']} - {details['ideal_for']}\n"
                )

        if context_type == "priority" and "emergency_procedures" in context:
            formatted_context += "\nEMERGENCY PROCEDURES:\n"
            for emergency, details in list(context["emergency_procedures"].items())[:2]:
                formatted_context += f"- {emergency}: {details['definition']} (Response time: {details['response_time']})\n"

        return formatted_context
