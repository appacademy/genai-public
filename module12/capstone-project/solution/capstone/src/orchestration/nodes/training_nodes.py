"""Training-related nodes for the HR assistant orchestration graph."""

import time
import pandas as pd
from src.orchestration.utils import log_processing_time


def training_lookup(state, training_records, diagnostics, memory):
    """Generate a response with the employee's training record."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=["training_records"],
    )

    # Get employee records
    employee_records = training_records.get_employee_record(state.employee_id)
    snapshot_path = training_records.create_snapshot(state.employee_id)

    # Generate the response
    response = f"Here's your current training record:\n\n"
    if len(employee_records) == 0:
        response += "You are not currently enrolled in any training courses."
    else:
        for _, record in employee_records.iterrows():
            status = record["status"]
            course = f"{record['course_id']}: {record['course_name']}"

            # Format enrollment date if available
            enrolled = ""
            if "enrolled_date" in record and pd.notna(record["enrolled_date"]):
                enrolled = f"Enrolled: {record['enrolled_date']}"

            # Format completion date
            completion = (
                record["completion_date"]
                if pd.notna(record["completion_date"])
                else "Not completed"
            )

            # Format due date
            due = (
                f"Due: {record['due_date']}"
                if pd.notna(record["due_date"])
                else "No due date"
            )

            # Include enrollment date in the display
            if enrolled:
                response += (
                    f"• {course} - {status} ({enrolled}, {completion}) - {due}\n"
                )
            else:
                response += f"• {course} - {status} ({completion}) - {due}\n"

    response += (
        f"\nA snapshot of your training record has been saved to {snapshot_path}."
    )

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training lookup", start_time)

    return {"response": response}


def training_courses(state, training_records, diagnostics, memory):
    """Generate a response with available training courses."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=(state.previous_question is not None),
        detected_entities=["course_catalog"],
    )

    # Load courses from catalog
    courses_df = training_records.load_courses()

    # Check if we need to filter by category
    category = None
    query_lower = state.user_input.lower()
    if "mandatory" in query_lower or "required" in query_lower:
        category = "Mandatory"
        filtered_courses = training_records.get_available_courses(category=category)
        response = "Here are the mandatory/required courses:\n\n"
    elif "elective" in query_lower or "optional" in query_lower:
        category = "Elective"
        filtered_courses = training_records.get_available_courses(category=category)
        response = "Here are the elective/optional courses:\n\n"
    else:
        filtered_courses = courses_df
        response = "Here are all available training courses:\n\n"

    # Generate response
    if len(filtered_courses) == 0:
        response = "No courses are currently available in the catalog."
    else:
        # Group by category if not already filtered
        if category is None:
            # First list mandatory courses
            mandatory = training_records.get_available_courses(category="Mandatory")
            if len(mandatory) > 0:
                response += "🛡️ MANDATORY COURSES (required):\n"
                for _, course in mandatory.iterrows():
                    renewal = (
                        f" (Renewal: {course['renewal_period']})"
                        if pd.notna(course["renewal_period"])
                        else ""
                    )
                    response += (
                        f"• {course['course_code']}: {course['title']}{renewal}\n"
                    )
                response += "\n"

            # Then list elective courses
            elective = training_records.get_available_courses(category="Elective")
            if len(elective) > 0:
                response += "📚 ELECTIVE COURSES (optional):\n"
                for _, course in elective.iterrows():
                    response += f"• {course['course_code']}: {course['title']}\n"

        else:
            # List courses in the filtered category
            for _, course in filtered_courses.iterrows():
                if category == "Mandatory":
                    renewal = (
                        f" (Renewal: {course['renewal_period']})"
                        if pd.notna(course["renewal_period"])
                        else ""
                    )
                    response += (
                        f"• {course['course_code']}: {course['title']}{renewal}\n"
                    )
                else:
                    response += f"• {course['course_code']}: {course['title']}\n"

    # Add instructions for enrollment
    response += "\nTo enroll in a course, say 'Enroll me in [COURSE CODE]'"

    # Add information about compliance if applicable
    if category == "Mandatory" or category is None:
        response += "\nTo check your compliance status, say 'Am I compliant with mandatory training?'"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training courses lookup", start_time)

    return {"response": response}


def training_enroll(state, training_records, diagnostics, memory):
    """Enroll an employee in one or more training courses."""
    start_time = time.time()

    # Get course IDs from intent args
    course_ids = state.intent["args"].get("course_ids", [])

    # Ensure we always have a list, even if only one course ID was provided
    if not isinstance(course_ids, list):
        course_ids = [course_ids]

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=[
            "course_enrollment",
            f"course_ids:{','.join(course_ids)}",
        ],
    )

    # Process each course ID
    results = []
    for course_id in course_ids:
        # In a real system, we'd look up the course name from a course catalog
        course_name = f"Course {course_id}"

        success, message = training_records.enroll_in_course(
            state.employee_id, course_id, course_name
        )
        results.append((course_id, success, message))

    # Generate the response based on the results
    if len(results) == 1:
        # Single course enrollment
        course_id, success, message = results[0]
        if success:
            response = f"You've been successfully enrolled in {course_id}."
        else:
            response = f"Enrollment failed for {course_id}: {message}"
    else:
        # Multiple course enrollments
        response = "I've processed your course enrollments:\n\n"
        success_count = 0
        for course_id, success, message in results:
            if success:
                response += f"• {course_id}: Successfully enrolled\n"
                success_count += 1
            else:
                response += f"• {course_id}: Failed - {message}\n"

        if success_count == len(results):
            response = (
                f"You've been successfully enrolled in all {len(results)} courses:\n\n"
                + "\n".join([f"• {r[0]}" for r in results])
            )
        elif success_count == 0:
            response = (
                "I was unable to enroll you in any of the courses:\n\n"
                + "\n".join([f"• {r[0]}: {r[2]}" for r in results])
            )

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training enrollment", start_time)

    return {"response": response}


def training_update(state, training_records, diagnostics, memory):
    """Mark one or more training courses as completed."""
    start_time = time.time()

    # Get course IDs from intent args
    course_ids = state.intent["args"].get("course_ids", [])

    # Ensure we always have a list, even if only one course ID was provided
    if not isinstance(course_ids, list):
        course_ids = [course_ids]

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=[
            "course_completion",
            f"course_ids:{','.join(course_ids)}",
        ],
    )

    # Process each course ID
    results = []
    for course_id in course_ids:
        success, message = training_records.update_completion(
            state.employee_id, course_id
        )
        results.append((course_id, success, message))

    # Generate the response based on the results
    if len(results) == 1:
        # Single course update
        course_id, success, message = results[0]
        if success:
            response = f"Great job! I've marked {course_id} as completed."
        else:
            response = f"Update failed for {course_id}: {message}"
    else:
        # Multiple course updates
        response = "I've processed your course completions:\n\n"
        success_count = 0
        for course_id, success, message in results:
            if success:
                response += f"• {course_id}: Successfully marked as completed\n"
                success_count += 1
            else:
                response += f"• {course_id}: Failed - {message}\n"

        if success_count == len(results):
            response = (
                f"Great job! I've marked all {len(results)} courses as completed:\n\n"
                + "\n".join([f"• {r[0]}" for r in results])
            )
        elif success_count == 0:
            response = "I was unable to update any of the courses:\n\n" + "\n".join(
                [f"• {r[0]}: {r[2]}" for r in results]
            )

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Training update", start_time)

    return {"response": response}


def mandatory_training(state, training_records, diagnostics, memory):
    """Enroll an employee in all mandatory courses."""
    start_time = time.time()

    # Log the request
    diagnostics.log_query_processing(
        query=state.user_input,
        is_followup=False,
        detected_entities=["mandatory_training", "batch_enrollment"],
    )

    # Process mandatory enrollments
    results = training_records.enroll_mandatory_courses(state.employee_id)

    # Generate response
    response = "I've processed your mandatory training enrollment:\n\n"
    for course_id, success, message in results:
        if success:
            response += f"• Enrolled in {course_id}\n"
        else:
            response += f"• {course_id}: {message}\n"

    # Update memory with this interaction
    memory.update(state)

    log_processing_time("Mandatory training enrollment", start_time)

    return {"response": response}
