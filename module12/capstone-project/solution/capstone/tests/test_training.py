import unittest
import os
import shutil
import pandas as pd
from src.training.csv_tools import TrainingRecords


class TestTrainingRecords(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create test directories
        self.test_dir = "test_data_training"
        self.master_path = f"{self.test_dir}/master.csv"
        self.snapshot_dir = f"{self.test_dir}/snapshots"

        # Initialize training records with test paths
        self.training_records = TrainingRecords(
            master_path=self.master_path, snapshot_dir=self.snapshot_dir
        )

    def tearDown(self):
        """Clean up test environment after each test"""
        # Remove test directories
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_course_catalog(self):
        """Test loading the course catalog"""
        # First, create a test course catalog
        courses_df = pd.DataFrame(
            [
                {
                    "course_code": "TEST-001",
                    "title": "Test Course",
                    "description": "A test course",
                    "format": "Online",
                    "category": "Mandatory",
                    "compliance_goal": "Test compliance",
                    "renewal_period": "12 months",
                }
            ]
        )
        courses_df.to_csv(f"{self.test_dir}/courses.csv", index=False)

        # Set the courses path
        self.training_records.courses_path = f"{self.test_dir}/courses.csv"

        # Load courses
        loaded_courses = self.training_records.load_courses()

        # Check that the course was loaded correctly
        self.assertEqual(len(loaded_courses), 1)
        self.assertEqual(loaded_courses.iloc[0]["course_code"], "TEST-001")
        self.assertEqual(loaded_courses.iloc[0]["title"], "Test Course")

    def test_get_available_courses(self):
        """Test getting available courses"""
        # Create test course catalog with multiple categories
        courses_df = pd.DataFrame(
            [
                {
                    "course_code": "MAND-001",
                    "title": "Mandatory Course",
                    "description": "A mandatory course",
                    "format": "Online",
                    "category": "Mandatory",
                    "compliance_goal": "Test compliance",
                    "renewal_period": "12 months",
                },
                {
                    "course_code": "ELECT-001",
                    "title": "Elective Course",
                    "description": "An elective course",
                    "format": "Online",
                    "category": "Elective",
                    "compliance_goal": "",
                    "renewal_period": "",
                },
            ]
        )
        courses_df.to_csv(f"{self.test_dir}/courses.csv", index=False)

        # Set the courses path
        self.training_records.courses_path = f"{self.test_dir}/courses.csv"

        # Get all courses
        all_courses = self.training_records.get_available_courses()
        self.assertEqual(len(all_courses), 2)

        # Get mandatory courses
        mandatory_courses = self.training_records.get_available_courses(
            category="Mandatory"
        )
        self.assertEqual(len(mandatory_courses), 1)
        self.assertEqual(mandatory_courses.iloc[0]["course_code"], "MAND-001")

        # Get elective courses
        elective_courses = self.training_records.get_available_courses(
            category="Elective"
        )
        self.assertEqual(len(elective_courses), 1)
        self.assertEqual(elective_courses.iloc[0]["course_code"], "ELECT-001")

    def test_check_compliance_status(self):
        """Test checking compliance status"""
        # Create test course catalog
        courses_df = pd.DataFrame(
            [
                {
                    "course_code": "HR-001",
                    "title": "Mandatory Course 1",
                    "description": "A mandatory course",
                    "format": "Online",
                    "category": "Mandatory",
                    "compliance_goal": "Test compliance",
                    "renewal_period": "12 months",
                },
                {
                    "course_code": "SEC-010",
                    "title": "Mandatory Course 2",
                    "description": "Another mandatory course",
                    "format": "Online",
                    "category": "Mandatory",
                    "compliance_goal": "Test compliance",
                    "renewal_period": "6 months",
                },
            ]
        )
        courses_df.to_csv(f"{self.test_dir}/courses.csv", index=False)

        # Create test records
        records_df = pd.DataFrame(
            [
                {
                    "employee_id": "test_employee",
                    "employee_name": "Test Employee",
                    "course_code": "HR-001",
                    "status": "Completed",
                    "completion_date": "2025-01-01",
                    "due_date": "2026-01-01",
                },
                {
                    "employee_id": "test_employee",
                    "employee_name": "Test Employee",
                    "course_code": "SEC-010",
                    "status": "Enrolled",
                    "completion_date": None,
                    "due_date": "2025-10-01",
                },
            ]
        )
        records_df.to_csv(f"{self.test_dir}/records.csv", index=False)

        # Set the paths
        self.training_records.courses_path = f"{self.test_dir}/courses.csv"
        self.training_records.records_path = f"{self.test_dir}/records.csv"

        # Check compliance status
        compliance = self.training_records.check_compliance_status("test_employee")

        # Should be two entries
        self.assertEqual(len(compliance), 2)

        # HR-001 should be compliant
        hr_status = [s for s in compliance if s["course_code"] == "HR-001"][0]
        self.assertEqual(hr_status["status"], "Completed")
        self.assertTrue(hr_status["compliance"])

        # SEC-010 should be non-compliant (not completed)
        sec_status = [s for s in compliance if s["course_code"] == "SEC-010"][0]
        self.assertEqual(sec_status["status"], "Enrolled")
        self.assertFalse(sec_status["compliance"])

    def test_master_csv_creation(self):
        """Test that the master CSV is created correctly"""
        # The constructor should create the master CSV
        self.assertTrue(os.path.exists(self.master_path))

        # Check that it has the expected columns
        df = pd.read_csv(self.master_path)
        expected_columns = [
            "employee_id",
            "course_id",
            "course_name",
            "status",
            "enrolled_date",
            "completion_date",
            "due_date",
        ]
        for col in expected_columns:
            self.assertIn(col, df.columns)

    def test_course_enrollment(self):
        """Test enrolling in a course"""
        # Enroll in a course
        employee_id = "test_employee"
        course_id = "TEST-101"
        course_name = "Test Course"

        success, message = self.training_records.enroll_in_course(
            employee_id, course_id, course_name
        )

        # Check that enrollment was successful
        self.assertTrue(success)
        self.assertIn("Successfully enrolled", message)

        # Check that the record was added to the master CSV
        df = pd.read_csv(self.master_path)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["employee_id"], employee_id)
        self.assertEqual(df.iloc[0]["course_id"], course_id)
        self.assertEqual(df.iloc[0]["course_name"], course_name)
        self.assertEqual(df.iloc[0]["status"], "Enrolled")

        # Check that a snapshot was created
        snapshots = os.listdir(self.snapshot_dir)
        self.assertEqual(len(snapshots), 1)
        self.assertTrue(snapshots[0].startswith(employee_id))

    def test_duplicate_enrollment(self):
        """Test that duplicate enrollments are prevented"""
        # Enroll in a course
        employee_id = "test_employee"
        course_id = "TEST-101"
        course_name = "Test Course"

        # First enrollment should succeed
        success1, _ = self.training_records.enroll_in_course(
            employee_id, course_id, course_name
        )

        # Second enrollment should fail
        success2, message2 = self.training_records.enroll_in_course(
            employee_id, course_id, course_name
        )

        # Check results
        self.assertTrue(success1)
        self.assertFalse(success2)
        self.assertIn("Already enrolled", message2)

    def test_completion_update(self):
        """Test updating course completion status"""
        # Enroll in a course
        employee_id = "test_employee"
        course_id = "TEST-101"
        course_name = "Test Course"

        self.training_records.enroll_in_course(employee_id, course_id, course_name)

        # Mark as completed
        success, message = self.training_records.update_completion(
            employee_id, course_id
        )

        # Check that update was successful
        self.assertTrue(success)
        self.assertIn("Marked", message)

        # Check that the record was updated in the master CSV
        df = pd.read_csv(self.master_path)
        self.assertEqual(df.iloc[0]["status"], "Completed")
        self.assertIsNotNone(df.iloc[0]["completion_date"])

    def test_nonexistent_course_update(self):
        """Test updating a course that doesn't exist"""
        employee_id = "test_employee"
        course_id = "NONEXISTENT"

        # Try to mark a non-existent course as completed
        success, message = self.training_records.update_completion(
            employee_id, course_id
        )

        # Check that update failed
        self.assertFalse(success)
        self.assertIn("No enrollment found", message)

    def test_employee_record_retrieval(self):
        """Test retrieving an employee's training record"""
        # Enroll in multiple courses
        employee_id = "test_employee"
        courses = [
            ("TEST-101", "Test Course 1"),
            ("TEST-102", "Test Course 2"),
            ("TEST-103", "Test Course 3"),
        ]

        for course_id, course_name in courses:
            self.training_records.enroll_in_course(employee_id, course_id, course_name)

        # Retrieve the employee's record
        record = self.training_records.get_employee_record(employee_id)

        # Check that all courses are in the record
        self.assertEqual(len(record), 3)
        course_ids = record["course_id"].tolist()
        for course_id, _ in courses:
            self.assertIn(course_id, course_ids)

    def test_mandatory_courses_enrollment(self):
        """Test enrolling in mandatory courses"""
        employee_id = "test_employee"

        # Enroll in mandatory courses
        results = self.training_records.enroll_mandatory_courses(employee_id)

        # Check that all enrollments were successful
        self.assertEqual(len(results), 3)  # There should be 3 mandatory courses
        for course_id, success, _ in results:
            self.assertTrue(success)

        # Check that the courses were added to the master CSV
        df = pd.read_csv(self.master_path)
        self.assertEqual(len(df), 3)

        # Check that a snapshot was created
        snapshots = os.listdir(self.snapshot_dir)
        self.assertGreaterEqual(len(snapshots), 1)


if __name__ == "__main__":
    unittest.main()
