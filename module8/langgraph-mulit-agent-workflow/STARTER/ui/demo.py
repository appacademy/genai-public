from langchain_core.messages import AIMessage


def run_demo(process_inquiry_func):
    """Run a demonstration with example inquiries."""
    examples = [
        {
            "inquiry": "I was charged twice for my subscription last month and need a refund.",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "context": "Pro plan, Account #12345, Charges on 3/15 and 3/16",
        },
        {
            "inquiry": "My account is locked and I can't reset my password. I've tried multiple times.",
            "name": "Sarah Johnson",
            "email": "sarah.j@example.com",
            "context": "Using Chrome browser, 2FA enabled",
        },
        {
            "inquiry": "Does your premium plan include API access? I need details on rate limits.",
            "name": None,
            "email": None,
            "context": None,
        },
        {
            "inquiry": "This is an emergency! My business account is showing $0 balance and all my client data is missing!",
            "name": "Michael Chen",
            "email": "mchen@business.com",
            "context": "Enterprise plan, 50+ users affected",
        },
    ]

    print("\n" + "=" * 60)
    print("                 RUNNING DEMO")
    print("=" * 60)

    for i, example in enumerate(examples, 1):
        # Format and display the example
        display_text = f'\nExample {i}: "{example["inquiry"]}"'
        if any([example["name"], example["email"], example["context"]]):
            display_text += "\nUser information provided:"
            if example["name"]:
                display_text += f"\n- Name: {example['name']}"
            if example["email"]:
                display_text += f"\n- Email: {example['email']}"
            if example["context"]:
                display_text += f"\n- Additional context: {example['context']}"
        else:
            display_text += "\nNo additional user information provided"

        print(display_text)
        print("-" * 40)
        print("Processing inquiry...")

        # Process the example
        result = process_inquiry_func(
            example["inquiry"],
            user_name=example["name"],
            user_email=example["email"],
            additional_context=example["context"],
        )

        # Display classification
        for message in result["messages"][1:2]:  # Just the classification message
            print(f"\nClassification: {message.content}")

        # Display response (skip user message and classification)
        print("\nResponse:")
        for message in result["messages"][2:]:
            if isinstance(message, AIMessage):
                print(message.content)

        print("\n" + "=" * 60)

        # Pause between examples unless it's the last one
        if i < len(examples):
            input("Press Enter to continue to the next example...")

    print("\nDemo completed. You can now enter your own inquiries.")
    print("=" * 60 + "\n")
