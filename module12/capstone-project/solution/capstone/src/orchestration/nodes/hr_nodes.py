"""HR administration nodes for the HR assistant orchestration graph."""

import time
import pandas as pd
from datetime import datetime, timedelta
from src.orchestration.utils import log_processing_time
from src.employee.employee_info import EmployeeManager
from src.training.csv_tools import TrainingRecords


def hr_employees(state, diagnostics, memory):
    """Generate a response with the employee directory."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_directory"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access the employee directory. Please contact HR if you need this information."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Load and format employee data
    try:
        employees_df = pd.read_csv("data/employees.csv")

        response = "## EMPLOYEE DIRECTORY\n\n"
        for _, emp in employees_df.iterrows():
            # Ensure we're handling the columns in the right order
            department = emp.get("department", "")
            role = emp.get("role", "")
            start_date = emp.get("start_date", "")

            # Format the display string properly
            response += f"• {emp['employee_id']}: {emp['name']} - {department}, {role} (Started: {start_date})\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing employee data: {str(e)}"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR employee directory access", start_time)

    return {"response": response}


def hr_training(state, diagnostics, memory):
    """Generate a response with all training records."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "training_records"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access all training records. Please contact HR if you need this information."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Load and format training data
    try:
        training_df = pd.read_csv("data/training/master.csv")

        response = "## MASTER TRAINING RECORDS\n\n"

        # Group by employee and course
        training_df = training_df.sort_values(["employee_id", "course_id"])

        current_employee = None
        for _, record in training_df.iterrows():
            if current_employee != record["employee_id"]:
                current_employee = record["employee_id"]
                response += (
                    f"\n### {record['employee_name']} ({record['employee_id']})\n"
                )

            status = record["status"]
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            response += f"• {record['course_id']}: {status} ({completion}) - {due}\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing training records: {str(e)}"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR training records access", start_time)

    return {"response": response}


def hr_employee_training(state, diagnostics, memory):
    """Generate a response with a specific employee's training records."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_training"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access training records for other employees. Please contact HR if you need this information."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Try to extract employee name from the query
    query_lower = state.user_input.lower()
    employee_name = None

    try:
        employees_df = pd.read_csv("data/employees.csv")
        for _, emp in employees_df.iterrows():
            name_parts = emp["name"].lower().split()
            # Check if any part of the employee name is in the query
            for part in name_parts:
                if part in query_lower and len(part) > 2:  # Avoid matching common words
                    employee_name = emp["name"]
                    employee_id = emp["employee_id"]
                    break
            if employee_name:
                break

        if not employee_name:
            response = "I couldn't identify which employee's training records you want to view. Please specify the employee name clearly."
            return {"response": response}

        # Load and format training data for the specific employee
        training_df = pd.read_csv("data/training/master.csv")
        employee_records = training_df[training_df["employee_id"] == employee_id]

        if len(employee_records) == 0:
            response = f"No training records found for {employee_name}."
            return {"response": response}

        response = (
            f"## TRAINING RECORDS FOR {employee_name.upper()} ({employee_id})\n\n"
        )

        for _, record in employee_records.iterrows():
            status = record["status"]
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            response += f"• {record['course_id']}: {status} ({completion}) - {due}\n"

        response += "\nThis information is confidential and should only be accessed by HR personnel."

    except Exception as e:
        response = f"An error occurred accessing training records: {str(e)}"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR employee training access", start_time)

    return {"response": response}


def hr_update_employee(state, diagnostics, memory):
    """Update an existing employee's information."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "employee_update"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can update employee information. Please contact HR if you need this functionality."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to use this functionality. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Extract employee data from the intent
    if not state.intent.get("args"):
        response = (
            "No update information was provided. Please format your request with "
            "employee ID and the fields you want to update (name, department, role, or start_date)."
        )
        return {"response": response}

    args = state.intent["args"]
    employee_id = args.get("employee_id")

    if not employee_id:
        response = "No employee ID was provided. Please specify which employee you want to update."
        return {"response": response}

    # Collect fields to update
    update_data = {}
    if args.get("name"):
        update_data["name"] = args["name"]
    if args.get("department"):
        update_data["department"] = args["department"]
    if args.get("role"):
        update_data["role"] = args["role"]
    if args.get("start_date"):
        update_data["start_date"] = args["start_date"]

    if not update_data:
        response = "No update fields were provided. Please specify what information you want to update."
        return {"response": response}

    # Update the employee
    employee_manager = EmployeeManager()
    result = employee_manager.update_employee(employee_id, update_data)

    # Generate the response
    if result["success"]:
        response = f"## EMPLOYEE UPDATE SUCCESSFUL\n\n"
        response += f"Successfully updated employee {result['employee_id']}.\n\n"

        if "updated_data" in result:
            updated = result["updated_data"]
            response += "### Updated Information:\n"
            response += f"• Employee ID: {updated['employee_id']}\n"
            response += f"• Name: {updated['name']}\n"
            response += f"• Department: {updated['department']}\n"
            response += f"• Role: {updated['role']}\n"
            response += f"• Start Date: {updated['start_date']}\n"
    else:
        response = f"## EMPLOYEE UPDATE FAILED\n\n"
        response += f"{result['message']}"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR employee update", start_time)

    return {"response": response}


def hr_bulk_add_employees(state, diagnostics, memory, training_records):
    """Add multiple employees at once and enroll them in mandatory training."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "bulk_employee_add"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can add employees in bulk. Please contact HR if you need this functionality."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to use this functionality. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Extract employee data from the intent
    if not state.intent.get("args") or not state.intent["args"].get("employees"):
        response = (
            "No employee data was provided. Please format your request with "
            "employee details including employee_id, name, department, and role for each employee."
        )
        return {"response": response}

    employee_manager = EmployeeManager()
    employees_data = state.intent["args"]["employees"]

    # Add employees in bulk
    result = employee_manager.add_employees_bulk(employees_data)

    # Generate the response
    if result["success"]:
        response = f"## BULK EMPLOYEE ADDITION SUCCESSFUL\n\n"
        response += f"Successfully added {result['added']} out of {len(employees_data)} employees.\n\n"

        # List successfully added employees
        response += "### Successfully Added:\n"
        for detail in result["details"]:
            if detail["success"]:
                response += f"• {detail['employee_id']}: {detail['name']}\n"

        # List failed additions if any
        if result["failed"] > 0:
            response += "\n### Failed Additions:\n"
            for detail in result["details"]:
                if not detail["success"]:
                    response += f"• {detail['employee_id']}: {detail['name']} - {detail['message']}\n"

        # Now enroll successful employees in mandatory training
        response += "\n## MANDATORY TRAINING ENROLLMENT\n\n"

        training_results = {}
        for detail in result["details"]:
            if detail["success"]:
                # Enroll this employee in all mandatory courses
                training_result = training_records.enroll_mandatory_courses(
                    detail["employee_id"]
                )
                training_results[detail["employee_id"]] = {
                    "name": detail["name"],
                    "results": training_result,
                }

        # Format training enrollment results
        for employee_id, data in training_results.items():
            response += f"### {data['name']} ({employee_id}):\n"
            for course_id, success, message in data["results"]:
                if success:
                    response += f"• Enrolled in {course_id}\n"
                else:
                    response += f"• {course_id}: {message}\n"
            response += "\n"

    else:
        response = f"## BULK EMPLOYEE ADDITION FAILED\n\n"
        response += f"{result['message']}\n\n"

        if result["details"]:
            response += "### Errors:\n"
            for detail in result["details"]:
                response += f"• {detail['employee_id']}: {detail['name']} - {detail['message']}\n"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR bulk employee addition", start_time)

    return {"response": response}


def hr_analytics(state, diagnostics, memory):
    """Generate analytics responses to HR queries about training and employee data."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["hr_data_access", "analytics"],
    )

    # Check if user is Jane Doe (E002), the HR representative
    if state.employee_id != "E002" and not state.employee_id.startswith("guest_"):
        response = "Only the HR representative (Jane Doe, E002) can access analytics information. Please contact HR if you need this information."
        return {"response": response}

    # If it's a guest user or someone else, ask for HR credentials
    if state.employee_id != "E002":
        # This is a simplified authentication for demo purposes
        parts = state.user_input.lower().split()
        has_name = "jane" in parts and "doe" in parts
        has_id = "e002" in parts or "e-002" in parts

        if not (has_name and has_id):
            response = (
                "You need to provide the HR representative's credentials to view this information. "
                "Please include both the name (Jane Doe) and employee ID (E002) in your request."
            )
            return {"response": response}

    # Extract the query from the intent
    query = state.user_input.lower()

    try:
        # Load employee and training data
        employees_df = pd.read_csv("data/employees.csv")
        training_df = pd.read_csv("data/training/master.csv")

        # Process different types of analytical queries

        # Training completion queries
        if "complete" in query or "finish" in query or "done" in query:
            if "hr-001" in query or "hr001" in query:
                # Get HR-001 completion statistics
                hr001_records = training_df[training_df["course_id"] == "HR-001"]
                completed = hr001_records[
                    hr001_records["status"].isin(["Completed"])
                ].shape[0]
                total = hr001_records.shape[0]
                not_completed = total - completed

                response = f"## HR-001 Course Completion Analysis\n\n"
                response += f"• Total Enrollments: {total}\n"
                response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
                response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"

                # Add details of employees who haven't completed
                if "who" in query or "which" in query or "list" in query:
                    incomplete_records = hr001_records[
                        ~hr001_records["status"].isin(["Completed"])
                    ]
                    response += "### Employees Who Haven't Completed HR-001:\n"
                    for _, record in incomplete_records.iterrows():
                        status = record["status"]
                        response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"

            elif "hr-002" in query or "hr002" in query:
                # Get HR-002 completion statistics
                hr002_records = training_df[training_df["course_id"] == "HR-002"]
                completed = hr002_records[
                    hr002_records["status"].isin(["Completed"])
                ].shape[0]
                total = hr002_records.shape[0]
                not_completed = total - completed

                response = f"## HR-002 Course Completion Analysis\n\n"
                response += f"• Total Enrollments: {total}\n"
                response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
                response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"

                # Add details of employees who haven't completed
                if "who" in query or "which" in query or "list" in query:
                    incomplete_records = hr002_records[
                        ~hr002_records["status"].isin(["Completed"])
                    ]
                    response += "### Employees Who Haven't Completed HR-002:\n"
                    for _, record in incomplete_records.iterrows():
                        status = record["status"]
                        response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"

            elif "sec-010" in query or "sec010" in query:
                # Get SEC-010 completion statistics
                sec010_records = training_df[training_df["course_id"] == "SEC-010"]
                completed = sec010_records[
                    sec010_records["status"].isin(["Completed"])
                ].shape[0]
                total = sec010_records.shape[0]
                not_completed = total - completed

                response = f"## SEC-010 Course Completion Analysis\n\n"
                response += f"• Total Enrollments: {total}\n"
                response += f"• Completed: {completed} ({completed/total*100:.1f}%)\n"
                response += f"• Not Completed: {not_completed} ({not_completed/total*100:.1f}%)\n\n"

                # Add details of employees who haven't completed
                if "who" in query or "which" in query or "list" in query:
                    incomplete_records = sec010_records[
                        ~sec010_records["status"].isin(["Completed"])
                    ]
                    response += "### Employees Who Haven't Completed SEC-010:\n"
                    for _, record in incomplete_records.iterrows():
                        status = record["status"]
                        response += f"• {record['employee_name']} ({record['employee_id']}): {status}\n"

            else:
                # General completion statistics for all courses
                course_stats = {}
                for course_id in training_df["course_id"].unique():
                    course_records = training_df[training_df["course_id"] == course_id]
                    completed = course_records[
                        course_records["status"].isin(["Completed"])
                    ].shape[0]
                    total = course_records.shape[0]
                    not_completed = total - completed
                    course_stats[course_id] = {
                        "total": total,
                        "completed": completed,
                        "not_completed": not_completed,
                        "completion_rate": (
                            (completed / total * 100) if total > 0 else 0
                        ),
                    }

                response = f"## Training Completion Analysis\n\n"

                # Sort courses by completion rate
                sorted_courses = sorted(
                    course_stats.items(), key=lambda x: x[1]["completion_rate"]
                )

                for course_id, stats in sorted_courses:
                    response += f"### {course_id}:\n"
                    response += f"• Total Enrollments: {stats['total']}\n"
                    response += f"• Completed: {stats['completed']} ({stats['completion_rate']:.1f}%)\n"
                    response += f"• Not Completed: {stats['not_completed']} ({100-stats['completion_rate']:.1f}%)\n\n"

        # Department statistics
        elif "department" in query:
            # Get department statistics
            dept_counts = employees_df["department"].value_counts()
            total_employees = employees_df.shape[0]

            response = f"## Department Analysis\n\n"
            response += f"Total Employees: {total_employees}\n\n"

            for dept, count in dept_counts.items():
                if pd.notna(dept) and dept:  # Ensure department is not empty
                    percentage = (count / total_employees) * 100
                    response += f"• {dept}: {count} employees ({percentage:.1f}%)\n"

            # Add training completion by department if relevant
            if "training" in query or "course" in query or "complete" in query:
                response += "\n### Training Completion by Department\n\n"

                for dept in dept_counts.index:
                    if pd.notna(dept) and dept:  # Ensure department is not empty
                        dept_employees = employees_df[
                            employees_df["department"] == dept
                        ]["employee_id"].tolist()
                        dept_records = training_df[
                            training_df["employee_id"].isin(dept_employees)
                        ]

                        if not dept_records.empty:
                            completed = dept_records[
                                dept_records["status"] == "Completed"
                            ].shape[0]
                            total = dept_records.shape[0]
                            completion_rate = (
                                (completed / total) * 100 if total > 0 else 0
                            )

                            response += f"**{dept}**:\n"
                            response += f"• Course Enrollments: {total}\n"
                            response += (
                                f"• Completed: {completed} ({completion_rate:.1f}%)\n\n"
                            )

        # New employee statistics
        elif "new" in query and "employee" in query:
            # Define new employees as those who started within the last 30 days
            today = pd.Timestamp(datetime.now().date())
            cutoff_date = (today - pd.Timedelta(days=30)).strftime("%Y-%m-%d")

            new_employees = employees_df[employees_df["start_date"] >= cutoff_date]
            count_new = new_employees.shape[0]

            response = f"## New Employee Analysis\n\n"
            response += f"Total new employees (last 30 days): {count_new}\n\n"

            if count_new > 0:
                response += "### New Employees:\n"
                for _, emp in new_employees.iterrows():
                    response += f"• {emp['name']} ({emp['employee_id']}) - {emp['department']}, {emp['role']} (Started: {emp['start_date']})\n"

                # Add training enrollment status for new employees
                if "training" in query or "course" in query:
                    response += "\n### Training Status for New Employees\n\n"

                    new_emp_ids = new_employees["employee_id"].tolist()
                    for emp_id in new_emp_ids:
                        emp_name = new_employees[
                            new_employees["employee_id"] == emp_id
                        ]["name"].iloc[0]
                        response += f"**{emp_name} ({emp_id})**:\n"

                        emp_records = training_df[training_df["employee_id"] == emp_id]
                        if emp_records.empty:
                            response += "• No training courses enrolled\n\n"
                        else:
                            for _, record in emp_records.iterrows():
                                status = record["status"]
                                course = record["course_id"]
                                response += f"• {course}: {status}\n"
                            response += "\n"

        # Default response for unrecognized analytics queries
        else:
            response = (
                "I'm not sure what analytics you're looking for. You can ask about:\n\n"
                "• Course completion rates (e.g., 'How many people have completed HR-001?')\n"
                "• Department statistics (e.g., 'Show me department breakdown')\n"
                "• New employee information (e.g., 'How many new employees do we have?')\n"
                "• Training enrollment by department (e.g., 'What's the training status by department?')\n"
            )

    except Exception as e:
        response = f"An error occurred while generating analytics: {str(e)}"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("HR analytics", start_time)

    return {"response": response}
