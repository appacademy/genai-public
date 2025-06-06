import typer
from rich.console import Console
from rich.panel import Panel
import sys
from src.employee.employee_info import EmployeeInfo, EmployeeManager
import re


# Jenna signature for professional closing
JENNA_SIGNATURE = """
- Jenna
  AI HR Representative
  Gem City Technologies, Inc.
"""

# Exit indicators to detect when user wants to end the conversation
SOFT_EXIT_INDICATORS = [
    "bye",
    "goodbye",
    "no thanks",
    "that's all",
    "that will be all",
    "nothing else",
    "no more questions",
    "that's it",
    "we're done",
    "we are done",
]

# Hard exit indicators that completely terminate the application
HARD_EXIT_INDICATORS = [
    "exit",
    "quit",
    "exit application",
    "quit application",
    "terminate",
    "close",
    "shutdown",
]

# These are standalone words that should only exit if they're the entire message
STANDALONE_EXIT_WORDS = [
    "no",
    "nope",
    "done",
]


class ConsoleInterface:
    def __init__(self, workflow):
        self.workflow = workflow
        self.console = Console()
        self.app = typer.Typer()
        self.employee_manager = EmployeeManager()
        self.current_employee = None

    def show_new_employee_welcome(self, employee_name):
        """Display special welcome message for new employees"""
        welcome_text = f"""
        Welcome to Gem City Technologies, {employee_name}!
        
        I'm Jenna, your AI HR Assistant. I notice you're new here, so let me help you get started.
        
        Here are some key policies you might want to know about:
        • PTO Policy - Type "What's our PTO policy?" to learn more
        • Benefits Overview - Type "Tell me about our benefits"
        • Required Training - Type "Sign me up for all mandatory courses"
        
        Feel free to ask me any questions about our policies or procedures.
        """

        self.console.print(
            Panel(
                welcome_text.strip(), title="New Employee Welcome", border_style="green"
            )
        )

    def show_returning_employee_welcome(self, employee_name):
        """Display welcome message for returning employees"""
        welcome_text = f"""
        Welcome back, {employee_name}!
        
        I'm Jenna, your AI HR Assistant. How can I help you today?
        """

        self.console.print(
            Panel(welcome_text.strip(), title="Welcome Back", border_style="blue")
        )

    def show_welcome(self):
        """Display welcome message"""
        welcome_text = """
        Welcome to Jenna - Your AI HR Assistant!
        
        I can help you with:
        • Company policies and benefits questions
        • Training record lookup and management
        • Course enrollment and completion updates
        
        Type 'help' for more information or 'exit' to quit.
        """

        self.console.print(
            Panel(welcome_text.strip(), title="Jenna", subtitle="AI HR Assistant")
        )

    def show_help(self):
        """Display help information"""
        help_text = """
        Available commands:
        
        Policy & Benefits:
        • Ask any question about company policies or benefits
        • Example: "What's our PTO policy?" or "Tell me about our 401(k) match"
        
        Training Management:
        • "Show my training record" - View your current training status
        • "Enroll me in [COURSE-ID]" - Enroll in a specific course
        • "I finished [COURSE-ID]" - Mark a course as completed
        • "Sign me up for all mandatory courses" - Enroll in required training
        
        System:
        • "help" - Show this help message
        • "exit" - End the session
        """

        self.console.print(Panel(help_text.strip(), title="Help", border_style="blue"))

    def is_exit_intent(self, user_input):
        """Detect if the user intends to exit the conversation and what type of exit"""
        # TODO: Implement exit intent detection that:
        # 1. Checks for standalone exit words
        # 2. Identifies hard exit indicators (terminate application)
        # 3. Recognizes soft exit indicators (end conversation, restart)
        # 4. Returns the type of exit intent or False

        user_input_lower = user_input.lower().strip()

        # Check if the input exactly matches any standalone exit words
        if user_input_lower in STANDALONE_EXIT_WORDS:
            return "soft"

        # Check for hard exit indicators (terminate application)
        if any(indicator in user_input_lower for indicator in HARD_EXIT_INDICATORS):
            return "hard"

        # Check for soft exit indicators (end conversation, restart)
        if any(indicator in user_input_lower for indicator in SOFT_EXIT_INDICATORS):
            return "soft"

        # Not an exit intent
        return False

    def show_session_summary(self):
        """Generate and display a summary of the current session"""
        # This would typically track what the user has done in the session
        # For now, we'll just use a simple placeholder
        summary_text = f"""
        Thank you for using Jenna, {self.current_employee.name}!
        
        If you need assistance in the future, I'll be here to help with:
        • Policy and benefits inquiries
        • Training management
        • HR-related questions
        
        Have a great day!
        """

        return summary_text.strip()

    def show_goodbye_with_signature(self, exit_type="soft"):
        """Display goodbye message with signature"""
        if exit_type == "hard":
            # For full application exit
            goodbye_message = f"""
            {self.show_session_summary()}
            
            The application will now close. Goodbye!
            """

            self.console.print(
                Panel(
                    goodbye_message.strip(),
                    title="Session Complete",
                    border_style="green",
                )
            )

            # Format signature with Rich styling
            self.console.print("[dim]- [bold blue]Jenna[/bold blue][/dim]")
            self.console.print("[dim]  AI HR Representative[/dim]")
            self.console.print("[dim]  Gem City Technologies, Inc.[/dim]")

        else:
            # For conversation end with restart
            goodbye_message = f"""
            {self.show_session_summary()}
            
            If you need further assistance, I'll be ready after you log in again.
            """

            self.console.print(
                Panel(
                    goodbye_message.strip(),
                    title="Conversation Complete",
                    border_style="blue",
                )
            )

            # Format signature with Rich styling
            self.console.print("[dim]- [bold blue]Jenna[/bold blue][/dim]")
            self.console.print("[dim]  AI HR Representative[/dim]")
            self.console.print("[dim]  Gem City Technologies, Inc.[/dim]")

    def format_response(self, response):
        """Format response to preserve bullet points and line breaks while handling text wrapping"""
        # TODO: Implement response formatting that:
        # 1. Normalizes line breaks
        # 2. Preserves bullet points and numbered lists
        # 3. Maintains paragraph structure
        # 4. Handles special formatting elements
        # 5. Returns the properly formatted response

        if not response:
            return ""

        # First, normalize all line breaks to a standard format
        response = response.replace("\r\n", "\n").replace("\r", "\n")

        # Split the text into paragraphs and preserve bullet points
        paragraphs = []
        current_lines = []

        for line in response.split("\n"):
            # Check if the line is a bullet point or starts a new section
            is_bullet = re.match(r"^\s*[•*-]\s", line) is not None
            is_numbered = re.match(r"^\s*\d+\.\s", line) is not None
            is_heading = re.match(r"^\s*#{1,6}\s", line) is not None
            is_special_line = is_bullet or is_numbered or is_heading or not line.strip()

            # If it's a bullet point or starts a new section, store the previous lines as a paragraph
            if is_special_line and current_lines:
                paragraphs.append(" ".join(current_lines))
                current_lines = []

            # Add the current line (trimmed of excessive whitespace but preserving leading spaces for bullet points)
            if line.strip():
                if is_bullet or is_numbered:
                    # Preserve the bullet point formatting
                    current_lines.append(line.rstrip())
                else:
                    # For regular text, just add it, trimming excessive whitespace
                    current_lines.append(line.strip())
            elif not current_lines:
                # This is a blank line and we don't have accumulated text,
                # so add it as a paragraph separator
                paragraphs.append("")

        # Don't forget to add the last paragraph if there is one
        if current_lines:
            paragraphs.append(" ".join(current_lines))

        # Join paragraphs with line breaks
        return "\n".join(paragraphs)

    def process_input(self, user_input):
        """Process user input and return response"""
        # Check for system commands
        if user_input.lower() == "help":
            self.show_help()
            return None

        if self.is_exit_intent(user_input):
            self.show_goodbye_with_signature()
            return "EXIT_REQUESTED"

        # Process through workflow with employee context
        employee_context = {
            "user_input": user_input,
            "employee_id": self.current_employee.employee_id,
            "employee_name": self.current_employee.name,
            "is_new_employee": self.current_employee.is_new_employee,
        }

        # Add department and role if available
        if self.current_employee.department:
            employee_context["department"] = self.current_employee.department
        if self.current_employee.role:
            employee_context["role"] = self.current_employee.role

        result = self.workflow.invoke(employee_context)

        # LangGraph returns a dictionary-like object, so we need to access the response directly
        if hasattr(result, "response"):
            return result.response
        elif isinstance(result, dict) and "response" in result:
            return result["response"]
        else:
            # For debugging
            return f"Processed successfully, but no response format found. Result type: {type(result)}"

    def _initialize_employee(self, employee_name, employee_id):
        """Initialize employee information based on provided name and ID"""
        # Get employee info
        self.current_employee = self.employee_manager.get_employee(employee_id)

        if not self.current_employee:
            # Format employee_id to have consistent capitalization (uppercase first letter)
            formatted_employee_id = employee_id.upper() if employee_id else None

            # Try to get the employee again with the formatted ID just to be sure
            if formatted_employee_id and formatted_employee_id != employee_id:
                self.current_employee = self.employee_manager.get_employee(
                    formatted_employee_id
                )

            # Check if employee_id has valid format (e.g., starts with E followed by numbers)
            if (
                formatted_employee_id
                and (formatted_employee_id.startswith("E"))
                and formatted_employee_id[1:].isdigit()
            ):
                # Valid employee ID format - create a new employee with this ID
                self.console.print(
                    f"[yellow]Employee {formatted_employee_id} not found. Creating new employee profile.[/yellow]"
                )

                # Prompt for additional employee information
                department = self.console.input(
                    "[bold green]Department (optional, press Enter to skip):[/bold green] "
                )
                role = self.console.input(
                    "[bold green]Role (optional, press Enter to skip):[/bold green] "
                )

                # Default start date to today
                from datetime import datetime

                start_date = datetime.now()

                # Ask if user wants to specify a different start date
                custom_date = self.console.input(
                    "[bold green]Start date (YYYY-MM-DD, press Enter for today's date):[/bold green] "
                )
                if custom_date.strip():
                    try:
                        start_date = datetime.strptime(custom_date.strip(), "%Y-%m-%d")
                    except ValueError:
                        self.console.print(
                            "[yellow]Invalid date format. Using today's date instead.[/yellow]"
                        )

                # Create new employee with provided ID and additional information
                self.current_employee = EmployeeInfo(
                    employee_id=employee_id.upper(),  # Normalize to uppercase
                    name=employee_name,
                    department=department if department.strip() else None,
                    role=role if role.strip() else None,
                    start_date=start_date,
                    is_new_employee=True,
                )
                # Add to employee database
                self.employee_manager.add_employee(self.current_employee)
            else:
                # Invalid or empty employee ID - create a guest profile
                self.console.print(
                    "[yellow]Employee not found in the system. Creating guest profile.[/yellow]"
                )
                self.current_employee = EmployeeInfo(
                    employee_id="guest_" + employee_name.lower().replace(" ", "_"),
                    name=employee_name,
                    is_new_employee=True,
                )

        # Display appropriate welcome
        if self.current_employee.is_new_employee:
            self.show_new_employee_welcome(self.current_employee.name)
        else:
            self.show_returning_employee_welcome(self.current_employee.name)

        return self.current_employee

    def run_repl(self):
        """Run the main REPL loop with employee identification"""
        self.show_welcome()

        # Employee identification flow
        employee_name = self.console.input(
            "[bold green]Please enter your name:[/bold green] "
        )
        employee_id = self.console.input(
            "[bold green]Please enter your employee ID:[/bold green] "
        )

        # Initialize employee with the provided information
        self._initialize_employee(employee_name, employee_id)

        conversation_active = True
        task_completed = False
        conversation_counter = 0

        while conversation_active:
            try:
                # Get user input
                user_input = self.console.input("[bold green]You:[/bold green] ")

                # Skip empty inputs
                if not user_input.strip():
                    continue

                # Check for exit intent
                exit_intent = self.is_exit_intent(user_input)
                if exit_intent:
                    if exit_intent == "hard":
                        # Hard exit - completely terminate
                        self.show_goodbye_with_signature(exit_type="hard")
                        return  # Exit the application completely
                    else:
                        # Soft exit - show goodbye and restart
                        self.show_goodbye_with_signature(exit_type="soft")
                        # Instead of breaking, we'll restart the conversation
                        self.show_welcome()

                        # Re-initialize employee info
                        employee_name = self.console.input(
                            "[bold green]Please enter your name:[/bold green] "
                        )
                        employee_id = self.console.input(
                            "[bold green]Please enter your employee ID:[/bold green] "
                        )

                        # Get employee info and reset conversation
                        self._initialize_employee(employee_name, employee_id)
                        task_completed = False
                        conversation_counter = 0
                        continue

                # Process input
                response = self.process_input(user_input)

                # Display response (if any)
                if response:
                    # Add extra line before Jenna's response for better separation from debug output
                    print()
                    self.console.print("[bold blue]Jenna:[/bold blue]")

                    # Format the response to preserve bullet points and line breaks
                    formatted_response = self.format_response(response)

                    # Print each line of the formatted response
                    for line in formatted_response.split("\n"):
                        if line.strip():
                            self.console.print(line, soft_wrap=True, width=100)
                        else:
                            # Print empty line for paragraph breaks
                            self.console.print()

                    print()  # Extra line for readability

                    # Increment conversation counter and mark task as potentially completed
                    conversation_counter += 1
                    task_completed = True

                # After a few exchanges or when a task appears completed, ask if user needs anything else
                if task_completed and conversation_counter % 3 == 0:
                    task_completed = False

                    # Print the follow-up question first
                    self.console.print()
                    self.console.print(
                        "[bold blue]Jenna:[/bold blue] Is there anything else I can help you with today?"
                    )

                    # Then get user input on a new line with the normal prompt
                    follow_up = self.console.input("[bold green]You:[/bold green] ")

                    # Check if this is an exit intent
                    if not follow_up.strip():
                        continue

                    exit_intent = self.is_exit_intent(follow_up)
                    if exit_intent:
                        if exit_intent == "hard":
                            # Hard exit - completely terminate
                            self.show_goodbye_with_signature(exit_type="hard")
                            return  # Exit the application completely
                        else:
                            # Soft exit - show goodbye and restart
                            self.show_goodbye_with_signature(exit_type="soft")
                            # Instead of stopping the conversation, we'll restart it
                            self.show_welcome()

                            # Re-initialize employee info
                            employee_name = self.console.input(
                                "[bold green]Please enter your name:[/bold green] "
                            )
                            employee_id = self.console.input(
                                "[bold green]Please enter your employee ID:[/bold green] "
                            )

                            # Initialize employee with the provided information
                            self._initialize_employee(employee_name, employee_id)

                        # Reset conversation counters
                        task_completed = False
                        conversation_counter = 0
                    else:
                        # If not exiting, process this as a normal input
                        response = self.process_input(follow_up)

                        # Check if this was an exit intent that we missed
                        if response == "EXIT_REQUESTED":
                            # Restart the conversation
                            self.show_welcome()

                            # Re-initialize employee info
                            employee_name = self.console.input(
                                "[bold green]Please enter your name:[/bold green] "
                            )
                            employee_id = self.console.input(
                                "[bold green]Please enter your employee ID:[/bold green] "
                            )

                            # Initialize employee using our case-insensitive method
                            self._initialize_employee(employee_name, employee_id)

                            # Display appropriate welcome
                            if self.current_employee.is_new_employee:
                                self.show_new_employee_welcome(
                                    self.current_employee.name
                                )
                            else:
                                self.show_returning_employee_welcome(
                                    self.current_employee.name
                                )

                            # Reset conversation counters
                            task_completed = False
                            conversation_counter = 0

                        # Display response
                        if response:
                            print()
                            self.console.print("[bold blue]Jenna:[/bold blue]")

                            # Format and print the response
                            formatted_response = self.format_response(response)
                            for line in formatted_response.split("\n"):
                                if line.strip():
                                    self.console.print(line, soft_wrap=True, width=100)
                                else:
                                    # Print empty line for paragraph breaks
                                    self.console.print()

                            print()

            except KeyboardInterrupt:
                print("\nExiting...")
                break

            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
