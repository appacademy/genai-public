import pandas as pd
import os
from datetime import datetime


class TrainingRecords:
    def __init__(
        self,
        master_path="data/training/master.csv",
        snapshot_dir="data/training/snapshots",
        courses_path="data/training/courses.csv",
    ):
        self.master_path = master_path
        self.snapshot_dir = snapshot_dir
        self.courses_path = courses_path

        # Ensure directories exist
        os.makedirs(os.path.dirname(master_path), exist_ok=True)
        os.makedirs(snapshot_dir, exist_ok=True)

        # Create master file if it doesn't exist
        if not os.path.exists(master_path):
            # Create with default columns
            df = pd.DataFrame(
                columns=[
                    "employee_id",
                    "employee_name",
                    "course_id",
                    "course_name",
                    "status",
                    "enrolled_date",
                    "completion_date",
                    "due_date",
                ]
            )
            df.to_csv(master_path, index=False)

        # Create courses file if it doesn't exist
        if not os.path.exists(courses_path):
            # Create with default columns
            df = pd.DataFrame(
                columns=[
                    "course_code",
                    "title",
                    "description",
                    "format",
                    "category",
                    "compliance_goal",
                    "renewal_period",
                ]
            )
            df.to_csv(courses_path, index=False)

    def load_master(self):
        """Load the master training records CSV"""
        return pd.read_csv(self.master_path)

    def save_master(self, df):
        """Save updated records to the master CSV"""
        df.to_csv(self.master_path, index=False)

    def get_employee_record(self, employee_id):
        """Get training records for a specific employee"""
        master_df = self.load_master()
        # Make employee_id case-insensitive
        employee_id_upper = employee_id.upper() if employee_id else None
        employee_df = master_df[
            master_df["employee_id"].str.upper() == employee_id_upper
        ]
        return employee_df

    def create_snapshot(self, employee_id):
        """Create a snapshot of an employee's training records"""
        employee_df = self.get_employee_record(employee_id)

        # If the employee records exist but don't have employee_name, add it
        if not employee_df.empty and (
            "employee_name" not in employee_df.columns
            or employee_df["employee_name"].isna().any()
        ):
            # Get employee name
            employee_name = self._get_employee_name(employee_id)

            # Add or update employee_name column
            employee_df["employee_name"] = employee_name

            # Also update the master record with this name
            self._update_master_record_name(employee_id, employee_name)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = os.path.join(
            self.snapshot_dir, f"{employee_id}_{timestamp}.csv"
        )
        employee_df.to_csv(snapshot_path, index=False)
        return snapshot_path

    def _update_master_record_name(self, employee_id, employee_name):
        """Update employee name in master records"""
        master_df = self.load_master()

        # Make employee_id case-insensitive
        employee_id_upper = employee_id.upper() if employee_id else None

        # Find all records for this employee
        mask = master_df["employee_id"].str.upper() == employee_id_upper

        if any(mask):
            # Update employee name for all records
            master_df.loc[mask, "employee_name"] = employee_name
            self.save_master(master_df)

    def enroll_in_course(self, employee_id, course_id, course_name, due_date=None):
        """Enroll an employee in a training course"""
        master_df = self.load_master()

        # Check if already enrolled
        existing = master_df[
            (master_df["employee_id"] == employee_id)
            & (master_df["course_id"] == course_id)
        ]

        if len(existing) > 0:
            return False, "Already enrolled in this course"

        # Get employee name
        employee_name = self._get_employee_name(employee_id)

        # Get today's date for enrollment
        today = datetime.now().strftime("%Y-%m-%d")

        # Add new enrollment
        new_row = {
            "employee_id": employee_id,
            "employee_name": employee_name,
            "course_id": course_id,
            "course_name": course_name,
            "status": "Enrolled",
            "enrolled_date": today,
            "completion_date": None,
            "due_date": due_date,
        }

        master_df = pd.concat([master_df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_master(master_df)

        # Create snapshot
        self.create_snapshot(employee_id)

        return True, f"Successfully enrolled in {course_id}"

    def _get_employee_name(self, employee_id):
        """Helper method to get employee name from various sources"""
        # First check master records
        master_df = self.load_master()
        # Make employee_id case-insensitive
        employee_id_upper = employee_id.upper() if employee_id else None
        master_records = master_df[
            master_df["employee_id"].str.upper() == employee_id_upper
        ]

        if (
            len(master_records) > 0
            and "employee_name" in master_records.columns
            and pd.notna(master_records.iloc[0].get("employee_name"))
        ):
            return master_records.iloc[0]["employee_name"]

        # Then try to get from employees.csv
        try:
            employees_path = "data/employees.csv"
            if os.path.exists(employees_path):
                employees_df = pd.read_csv(employees_path)
                # Make employee_id case-insensitive
                emp_record = employees_df[
                    employees_df["employee_id"].str.upper() == employee_id_upper
                ]
                if len(emp_record) > 0:
                    return emp_record.iloc[0]["name"]
        except:
            pass

        # If we have a guest user, try to extract name from ID (format: guest_name_format)
        if employee_id.startswith("guest_"):
            parts = employee_id.split("_")
            if len(parts) >= 2:
                # Convert to title case for nice formatting
                name_part = " ".join(parts[1:-1] if len(parts) > 2 else parts[1:])
                return name_part.replace("_", " ").title()

        # Default fallback
        return f"Employee {employee_id}"

    def update_completion(self, employee_id, course_id):
        """Mark a course as completed"""
        master_df = self.load_master()

        # Make employee_id case-insensitive
        employee_id_upper = employee_id.upper() if employee_id else None

        # Find the course enrollment
        mask = (master_df["employee_id"].str.upper() == employee_id_upper) & (
            master_df["course_id"] == course_id
        )

        if not any(mask):
            return False, f"No enrollment found for {course_id}"

        # Update status and completion date
        master_df.loc[mask, "status"] = "Completed"
        master_df.loc[mask, "completion_date"] = datetime.now().strftime("%Y-%m-%d")

        self.save_master(master_df)

        # Create snapshot
        self.create_snapshot(employee_id)

        return True, f"Marked {course_id} as completed"

    def load_courses(self):
        """Load the course catalog"""
        if os.path.exists(self.courses_path):
            return pd.read_csv(self.courses_path)
        return pd.DataFrame()

    # Removed the load_records and save_records methods as they're no longer needed

    def get_available_courses(self, category=None):
        """Get list of available courses, optionally filtered by category"""
        courses_df = self.load_courses()
        if category:
            return courses_df[courses_df["category"] == category]
        return courses_df

    def get_mandatory_courses(self):
        """Get list of mandatory courses"""
        return self.get_available_courses(category="Mandatory")

    def get_course_details(self, course_code):
        """Get details for a specific course"""
        courses_df = self.load_courses()
        course = courses_df[courses_df["course_code"] == course_code]
        if len(course) == 0:
            return None
        return course.iloc[0].to_dict()

    def check_compliance_status(self, employee_id):
        """Check if an employee is compliant with all mandatory training"""
        # TODO: Implement compliance checking that:
        # 1. Loads the master training records
        # 2. Gets the list of mandatory courses
        # 3. Checks if the employee has completed each mandatory course
        # 4. Verifies if completions are still valid based on renewal dates
        # 5. Returns a list of compliance status for each mandatory course

        master_df = self.load_master()
        mandatory_courses = self.get_mandatory_courses()

        # Filter records for this employee
        employee_records = master_df[master_df["employee_id"] == employee_id]

        # Check each mandatory course
        compliance_status = []
        for _, course in mandatory_courses.iterrows():
            course_code = course["course_code"]
            renewal_period = course["renewal_period"]

            # Check if employee has completed this course
            course_record = employee_records[
                employee_records["course_id"] == course_code
            ]

            if len(course_record) == 0:
                status = "Not Started"
                compliance = False
                due_date = None
            else:
                record = course_record.iloc[0]
                status = record["status"]
                due_date = record["due_date"]

                if status != "Completed":
                    compliance = False
                elif due_date and pd.notna(due_date):
                    # Check if still valid based on due date
                    compliance = pd.to_datetime(due_date) >= datetime.now()
                else:
                    compliance = True

            compliance_status.append(
                {
                    "course_code": course_code,
                    "title": course["title"],
                    "status": status,
                    "compliance": compliance,
                    "due_date": due_date,
                }
            )

        return compliance_status

    def get_upcoming_renewals(self, employee_id, days=30):
        """Get list of training courses that need renewal within specified days"""
        # TODO: Implement upcoming renewals detection that:
        # 1. Loads master training records
        # 2. Filters records for the specific employee
        # 3. Identifies courses with due dates within the specified time window
        # 4. Formats the results with course details and days remaining
        # 5. Returns a list of upcoming renewals sorted by due date

        master_df = self.load_master()

        # Filter records for this employee with due dates
        employee_records = master_df[
            (master_df["employee_id"] == employee_id) & (master_df["due_date"].notna())
        ]

        if len(employee_records) == 0:
            return []

        # Convert due dates to datetime
        employee_records["due_date"] = pd.to_datetime(employee_records["due_date"])

        # Calculate date threshold
        threshold = datetime.now() + pd.Timedelta(days=days)

        # Filter for records due within the threshold
        upcoming = employee_records[employee_records["due_date"] <= threshold]

        # Format results
        renewals = []
        for _, record in upcoming.iterrows():
            course_details = self.get_course_details(record["course_id"])
            if course_details:
                renewals.append(
                    {
                        "course_code": record["course_id"],
                        "title": course_details["title"],
                        "due_date": record["due_date"].strftime("%Y-%m-%d"),
                        "days_remaining": (record["due_date"] - datetime.now()).days,
                    }
                )

        return renewals

    def enroll_mandatory_courses(self, employee_id):
        """Enroll an employee in all mandatory courses"""
        # Get mandatory courses from the course catalog
        mandatory_df = self.get_mandatory_courses()

        results = []
        for _, course in mandatory_df.iterrows():
            course_id = course["course_code"]
            course_name = course["title"]

            # Calculate due date if there's a renewal period
            due_date = None
            if pd.notna(course["renewal_period"]):
                # Parse renewal period (assumes format like "12 months")
                try:
                    period_parts = str(course["renewal_period"]).split()
                    if len(period_parts) == 2 and period_parts[1].lower() in [
                        "month",
                        "months",
                    ]:
                        months = int(period_parts[0])
                        due_date = (
                            datetime.now() + pd.DateOffset(months=months)
                        ).strftime("%Y-%m-%d")
                except:
                    # If parsing fails, leave due_date as None
                    pass

            success, message = self.enroll_in_course(
                employee_id, course_id, course_name, due_date=due_date
            )
            results.append((course_id, success, message))

        # Create a final snapshot after all enrollments
        self.create_snapshot(employee_id)

        return results

    # Removed the _update_comprehensive_record method as it's no longer needed
