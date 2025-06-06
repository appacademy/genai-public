import os
import sys
from utils.input_parser import parse_user_input
from ui.demo import run_demo
from langchain_core.messages import AIMessage


def clear_screen():
    """Clear the console screen based on the operating system."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("           CUSTOMER SERVICE INQUIRY SYSTEM")
    print("=" * 60)
    print("\nThis system processes customer inquiries and routes them to")
    print("specialized agents based on the content and priority.")
    print("\nType 'exit' to quit, 'help' for assistance, 'demo' to see examples,")
    print("or enter your inquiry below.")
    print("\nTip: You can include optional name, email, and context information")
    print("in [brackets] for a more personalized response.")
    print(
        "Example: My account is locked [Name: Jane, Email: jane@example.com, Context: Pro plan]"
    )
    print("=" * 60 + "\n")


def print_help():
    """Print help information about the application."""
    print("\n" + "=" * 60)
    print("                      HELP")
    print("=" * 60)
    print(
        "\nThis application uses a multi-agent workflow to process customer inquiries."
    )
    print("\nYour inquiry will be:")
    print("1. Classified by type (billing, technical, product, or general)")
    print("2. Assigned a priority level (1-urgent to 4-low)")
    print("3. Routed to the appropriate specialized agent")
    print("4. Processed with relevant company knowledge and policies")
    print("5. Responded to with helpful information")
    print("\nExample inquiries you can try:")
    print("- 'I was charged twice for my subscription last month'")
    print("- 'I can't reset my password and I'm locked out of my account'")
    print("- 'What features are included in your Pro plan?'")
    print("- 'How do I contact your support team?'")
    print("- 'This is urgent! My account is showing all data deleted!'")
    print("\nYou can include optional information in [brackets] after your inquiry:")
    print("- Name: Your name for personalized responses")
    print("- Email: Your email address for follow-up")
    print("- Context: Additional details about your situation")
    print("\nExample with optional info:")
    print(
        "'I need to upgrade my plan [Name: John, Email: john@example.com, Context: Currently on Basic plan]'"
    )
    print("\nCommands:")
    print("- 'exit': Quit the application")
    print("- 'help': Display this help information")
    print("- 'clear': Clear the screen")
    print("- 'demo': Run a demonstration with example inquiries")
    print("=" * 60 + "\n")


def run_interactive_console(process_inquiry_func):
    """Run an interactive console for processing customer inquiries."""
    clear_screen()
    print_header()

    while True:
        user_input = input("\nEnter your inquiry (or command): ")

        # Handle commands
        if user_input.lower() == "exit":
            print("\nThank you for using the Customer Service Inquiry System. Goodbye!")
            break
        elif user_input.lower() == "help":
            print_help()
            continue
        elif user_input.lower() == "clear":
            clear_screen()
            print_header()
            continue
        elif user_input.lower() == "demo":
            run_demo(process_inquiry_func)
            continue

        # Check for empty input
        if not user_input.strip():
            print("Please enter a valid inquiry.")
            continue

        # Parse user input for optional information
        parsed_input = parse_user_input(user_input)

        # Display user information if provided
        if any(
            [
                parsed_input["name"],
                parsed_input["email"],
                parsed_input["additional_context"],
            ]
        ):
            print("\nIncluded information:")
            if parsed_input["name"]:
                print(f"- Name: {parsed_input['name']}")
            if parsed_input["email"]:
                print(f"- Email: {parsed_input['email']}")
            if parsed_input["additional_context"]:
                print(f"- Additional context: {parsed_input['additional_context']}")

        # Process the inquiry
        print("\nProcessing your inquiry...")
        result = process_inquiry_func(
            parsed_input["inquiry"],
            user_name=parsed_input["name"],
            user_email=parsed_input["email"],
            additional_context=parsed_input["additional_context"],
        )

        # Display the classification
        for message in result["messages"][1:2]:  # Just the classification message
            print(f"\nClassification: {message.content}")

        # Display the response (skip user message and classification)
        print("\n" + "=" * 60)
        print("                   RESPONSE")
        print("=" * 60)
        for message in result["messages"][2:]:
            if isinstance(message, AIMessage):
                print(message.content)
        print("=" * 60)
