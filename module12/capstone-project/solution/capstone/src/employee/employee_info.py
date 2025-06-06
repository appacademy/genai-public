from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta
import os
import csv


class EmployeeInfo(BaseModel):
    """Employee information model"""

    employee_id: str
    name: str
    start_date: Optional[datetime] = None
    department: Optional[str] = None
    role: Optional[str] = None
    is_new_employee: bool = False


class EmployeeManager:
    """Manages employee information"""

    def __init__(self, employee_file="data/employees.csv"):
        """Initialize the employee manager"""
        self.employee_file = employee_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the employee file if it doesn't exist"""
        if not os.path.exists(os.path.dirname(self.employee_file)):
            os.makedirs(os.path.dirname(self.employee_file))

        if not os.path.exists(self.employee_file):
            # Create a sample file with header row
            with open(self.employee_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["employee_id", "name", "department", "role", "start_date"]
                )
                # Add a few sample employees
                writer.writerow(
                    [
                        "EMP001",
                        "John Smith",
                        "Engineering",
                        "Software Engineer",
                        "2024-01-15",
                    ]
                )
                writer.writerow(
                    ["EMP002", "Jane Doe", "HR", "HR Specialist", "2024-04-22"]
                )
                writer.writerow(
                    [
                        "EMP003",
                        "Sam Wilson",
                        "Marketing",
                        "Marketing Manager",
                        "2023-11-10",
                    ]
                )

    def get_employee(self, employee_id: str) -> Optional[EmployeeInfo]:
        """Get employee information by ID"""
        if not os.path.exists(self.employee_file):
            return None

        # Normalize the employee_id to uppercase for case-insensitive comparison
        employee_id_upper = employee_id.upper() if employee_id else None

        with open(self.employee_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["employee_id"].upper() == employee_id_upper:
                    # Parse the start date
                    start_date = None
                    if row.get("start_date"):
                        try:
                            start_date = datetime.strptime(
                                row["start_date"], "%Y-%m-%d"
                            )
                        except ValueError:
                            pass

                    # Check if employee is new (started within the last 7 days)
                    is_new = False
                    if start_date:
                        today = datetime.now()
                        is_new = (today - start_date).days <= 7

                    return EmployeeInfo(
                        employee_id=row["employee_id"],
                        name=row["name"],
                        start_date=start_date,
                        department=row.get("department"),
                        role=row.get("role"),
                        is_new_employee=is_new,
                    )

        return None

    def find_employee_by_name(self, name: str) -> List[EmployeeInfo]:
        """Find employees by name (partial match)"""
        if not os.path.exists(self.employee_file):
            return []

        results = []
        name_lower = name.lower()

        with open(self.employee_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if name_lower in row["name"].lower():
                    # Parse the start date
                    start_date = None
                    if row.get("start_date"):
                        try:
                            start_date = datetime.strptime(
                                row["start_date"], "%Y-%m-%d"
                            )
                        except ValueError:
                            pass

                    # Check if employee is new (started within the last 7 days)
                    is_new = False
                    if start_date:
                        today = datetime.now()
                        is_new = (today - start_date).days <= 7

                    results.append(
                        EmployeeInfo(
                            employee_id=row["employee_id"],
                            name=row["name"],
                            start_date=start_date,
                            department=row.get("department"),
                            role=row.get("role"),
                            is_new_employee=is_new,
                        )
                    )

        return results

    def add_employee(self, employee: EmployeeInfo) -> bool:
        """Add a new employee to the database"""
        # Format the date
        start_date_str = ""
        if employee.start_date:
            start_date_str = employee.start_date.strftime("%Y-%m-%d")

        # Open file in append mode
        with open(self.employee_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    employee.employee_id,
                    employee.name,
                    employee.department or "",
                    employee.role or "",
                    start_date_str,
                ]
            )

        return True

    def update_employee(
        self, employee_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing employee's information in the database

        Parameters:
        - employee_id: The ID of the employee to update
        - update_data: Dictionary of fields to update with new values
                       Can include: name, department, role, start_date

        Returns:
        - Dictionary with operation result and updated employee data
        """
        if not os.path.exists(self.employee_file):
            return {
                "success": False,
                "message": "Employee database file does not exist",
                "employee_id": employee_id,
            }

        # Normalize the employee_id to uppercase for case-insensitive comparison
        employee_id_upper = employee_id.upper() if employee_id else None

        # Load the current employee data
        employees = []
        updated_employee = None
        employee_found = False

        with open(self.employee_file, "r") as f:
            reader = csv.DictReader(f)
            field_names = reader.fieldnames

            for row in reader:
                if row["employee_id"].upper() == employee_id_upper:
                    employee_found = True

                    # Update the fields that were provided
                    for field, value in update_data.items():
                        if field in row and value is not None:
                            row[field] = value

                    # Format date if it was provided as a datetime object
                    if "start_date" in update_data and isinstance(
                        update_data["start_date"], datetime
                    ):
                        row["start_date"] = update_data["start_date"].strftime(
                            "%Y-%m-%d"
                        )

                    updated_employee = row.copy()

                employees.append(row)

        if not employee_found:
            return {
                "success": False,
                "message": f"Employee with ID {employee_id} not found",
                "employee_id": employee_id,
            }

        # Write the updated data back to the file
        with open(self.employee_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(employees)

        return {
            "success": True,
            "message": f"Successfully updated employee {employee_id}",
            "employee_id": employee_id,
            "updated_data": updated_employee,
        }

    def add_employees_bulk(
        self, employees_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Add multiple employees to the database at once.

        Parameters:
        - employees_data: List of dictionaries with employee information
          Each dictionary should have keys: employee_id, name, department, role, start_date

        Returns:
        - Dictionary with success status and details
        """
        if not employees_data:
            return {
                "success": False,
                "message": "No employee data provided",
                "added": 0,
                "failed": 0,
                "details": [],
            }

        # Limit to maximum of 10 employees at once
        if len(employees_data) > 10:
            employees_data = employees_data[:10]

        results = []
        added_count = 0
        failed_count = 0

        for employee_data in employees_data:
            try:
                # Validate required fields
                if not employee_data.get("employee_id") or not employee_data.get(
                    "name"
                ):
                    results.append(
                        {
                            "employee_id": employee_data.get("employee_id", "Unknown"),
                            "name": employee_data.get("name", "Unknown"),
                            "success": False,
                            "message": "Missing required fields (employee_id and name)",
                        }
                    )
                    failed_count += 1
                    continue

                # Check if employee already exists
                existing_employee = self.get_employee(employee_data["employee_id"])
                if existing_employee:
                    results.append(
                        {
                            "employee_id": employee_data["employee_id"],
                            "name": employee_data["name"],
                            "success": False,
                            "message": f"Employee with ID {employee_data['employee_id']} already exists",
                        }
                    )
                    failed_count += 1
                    continue

                # Parse start date if present
                start_date = None
                if employee_data.get("start_date"):
                    try:
                        if isinstance(employee_data["start_date"], str):
                            start_date = datetime.strptime(
                                employee_data["start_date"], "%Y-%m-%d"
                            )
                        elif isinstance(employee_data["start_date"], datetime):
                            start_date = employee_data["start_date"]
                    except ValueError:
                        # If date parsing fails, default to today
                        start_date = datetime.now()
                else:
                    # Default to today if not provided
                    start_date = datetime.now()

                # Create and add the employee
                employee = EmployeeInfo(
                    employee_id=employee_data["employee_id"],
                    name=employee_data["name"],
                    department=employee_data.get("department"),
                    role=employee_data.get("role"),
                    start_date=start_date,
                    is_new_employee=True,
                )

                success = self.add_employee(employee)

                if success:
                    results.append(
                        {
                            "employee_id": employee_data["employee_id"],
                            "name": employee_data["name"],
                            "success": True,
                            "message": "Employee added successfully",
                        }
                    )
                    added_count += 1
                else:
                    results.append(
                        {
                            "employee_id": employee_data["employee_id"],
                            "name": employee_data["name"],
                            "success": False,
                            "message": "Failed to add employee",
                        }
                    )
                    failed_count += 1

            except Exception as e:
                results.append(
                    {
                        "employee_id": employee_data.get("employee_id", "Unknown"),
                        "name": employee_data.get("name", "Unknown"),
                        "success": False,
                        "message": f"Error: {str(e)}",
                    }
                )
                failed_count += 1

        return {
            "success": added_count > 0,
            "message": f"Added {added_count} employees, {failed_count} failed",
            "added": added_count,
            "failed": failed_count,
            "details": results,
        }
