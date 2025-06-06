from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Intent(BaseModel):
    intent: str = Field(description="The classified intent of the user query")
    args: Optional[Dict[str, Any]] = Field(
        None, description="Additional arguments extracted from the query"
    )


class IntentRouter:
    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser(pydantic_object=Intent)

        # Creating the intent classification prompt
        self.prompt = ChatPromptTemplate.from_template(
            """
        You are an HR assistant tasked with classifying user queries into specific intents.
        Analyze the following query and classify it into one of these intents:
        - policy_q: Questions about company policies (e.g., "What's our PTO policy?", "Tell me about our substance abuse policy") OR follow-up questions about policies (e.g., "How does it compare to X?", "Tell me more about it")
        - benefit_q: Questions about employee benefits (e.g., "What's our 401(k) match?", "What wellness programs do we offer?") OR follow-up questions about benefits
        - train_lookup: Requests to view training records (e.g., "Show my training record")
        - train_courses: Requests to list available courses or course catalog (e.g., "What courses are available?", "List the required courses", "What training courses do you offer?")
        - train_enroll: Requests to enroll in training courses (e.g., "Enroll me in SEC-230")
        - train_update: Notifications about completed training (e.g., "I finished AI-201")
        - train_mandatory: Requests for all mandatory training (e.g., "Sign me up for all mandatory courses")
        - hr_employees: Requests to view all employee data (e.g., "Show me all employees", "Display employee directory", "List all staff")
        - hr_training: Requests to view all training records (e.g., "Show me all training records", "Display training data", "View master training file")
        - hr_employee_training: Requests to view specific employee's training (e.g., "Show training for Alice Johnson", "View Carlos's training status")
        - hr_bulk_add: Requests to add multiple employees at once (e.g., "Add these employees: E012 John Smith IT, E013 Jane Brown Marketing", "Bulk add employees")
        - hr_update: Requests to update employee information (e.g., "Update employee E021 role to Department Manager", "Change Emma Jackson's department to Operations")
        - hr_analytics: Requests for HR analytics and statistics (e.g., "How many people have completed HR-001?", "Show department statistics", "Which employees haven't finished SEC-010?")
        - fallback: Any query not related to HR functions (e.g., "What's the weather?", "Tell me a joke")
        
        IMPORTANT: Questions about wellness programs, substance abuse, addiction support, mental health services, Employee Assistance Programs (EAP), and other sensitive HR topics should be classified as either policy_q or benefit_q depending on the nature of the question, NOT as fallback.
        
        For train_enroll, train_update, and train_mandatory, extract any relevant arguments.
        
        Examples:
        - "What's the weather today?" → {{"intent": "fallback"}}
        - "Tell me a joke" → {{"intent": "fallback"}}
        - "What's our PTO policy?" → {{"intent": "policy_q"}}
        - "Tell me about substance abuse policy" → {{"intent": "policy_q"}}
        - "What options do I have for addiction help?" → {{"intent": "policy_q"}}
        - "Does the wellness program address addiction?" → {{"intent": "benefit_q"}}
        - "Tell me about our Employee Assistance Program" → {{"intent": "benefit_q"}}
        - "What mental health resources are available?" → {{"intent": "benefit_q"}}
        - "Which takes precedence, Substance Abuse Policy or EAP?" → {{"intent": "policy_q"}}
        - "What courses are available?" → {{"intent": "train_courses"}}
        - "Can you list the required courses?" → {{"intent": "train_courses"}}
        - "What training do I need to take?" → {{"intent": "train_courses"}}
        - "Enroll me in SEC-230" → {{"intent": "train_enroll", "args": {{"course_ids": ["SEC-230"]}}}}
        - "Enroll me in SEC-230 and AI-201" → {{"intent": "train_enroll", "args": {{"course_ids": ["SEC-230", "AI-201"]}}}}
        - "I finished AI-201 yesterday" → {{"intent": "train_update", "args": {{"course_ids": ["AI-201"]}}}}
        - "I completed HR-001 and SEC-010" → {{"intent": "train_update", "args": {{"course_ids": ["HR-001", "SEC-010"]}}}}
        - "Add these employees: E012 John Smith IT, E013 Jane Doe HR" → {{"intent": "hr_bulk_add", "args": {{"employees": [
            {{"employee_id": "E012", "name": "John Smith", "department": "IT"}},
            {{"employee_id": "E013", "name": "Jane Doe", "department": "HR"}}
          ]}}}}
        - "Bulk add employees E014 Robert Jones Engineering and E015 Maria Garcia Marketing" → {{"intent": "hr_bulk_add", "args": {{"employees": [
            {{"employee_id": "E014", "name": "Robert Jones", "department": "Engineering"}},
            {{"employee_id": "E015", "name": "Maria Garcia", "department": "Marketing"}}
          ]}}}}
        - "Update employee E021 role to Department Manager" → {{"intent": "hr_update", "args": {{"employee_id": "E021", "role": "Department Manager"}}}}
        - "Change Emma Jackson's department to Operations" → {{"intent": "hr_update", "args": {{"employee_id": "E021", "name": "Emma Jackson", "department": "Operations"}}}}
        - "Set E015 start date to 2025-01-15" → {{"intent": "hr_update", "args": {{"employee_id": "E015", "start_date": "2025-01-15"}}}}
        - "Update James Anderson to the role of Senior Account Executive" → {{"intent": "hr_update", "args": {{"employee_id": "E020", "name": "James Anderson", "role": "Senior Account Executive"}}}}
        
        User query: {query}
        
        Classification (output as JSON):
        """
        )

        self.chain = self.prompt | self.llm | self.parser

    def classify(self, query):
        """Classify a user query into an intent"""
        return self.chain.invoke({"query": query})
