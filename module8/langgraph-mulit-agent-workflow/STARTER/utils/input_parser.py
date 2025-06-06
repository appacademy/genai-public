import re


def parse_user_input(input_text):
    """Extract inquiry content and optional user information."""
    # Default values
    inquiry = input_text
    name = None
    email = None
    context = None

    # Look for optional format with square brackets
    bracket_match = re.search(r"(.*?)(?:\[(.*?)\])?$", input_text)
    if bracket_match and bracket_match.group(2):
        inquiry = bracket_match.group(1).strip()
        info_text = bracket_match.group(2).strip()

        # Extract name if provided
        name_match = re.search(r"Name:\s*(.*?)(?:,|$)", info_text)
        if name_match:
            name = name_match.group(1).strip()

        # Extract email if provided
        email_match = re.search(r"Email:\s*(.*?)(?:,|$)", info_text)
        if email_match:
            email = email_match.group(1).strip()

        # Extract additional context if provided
        context_match = re.search(r"Context:\s*(.*?)(?:,|$)", info_text)
        if context_match:
            context = context_match.group(1).strip()

    return {
        "inquiry": inquiry,
        "name": name,
        "email": email,
        "additional_context": context,
    }
